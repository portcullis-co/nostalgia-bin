import json
import numpy as np
import pandas as pd
import clickhouse_connect
from openai import OpenAI
from tqdm.auto import tqdm
import datetime
import os

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  # Make sure OPENAI_API_KEY is set in your environment

# Function to get embeddings from OpenAI
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",  # 1536 dimensions
        input=text
    )
    return response.data[0].embedding

# Load the generated product data
with open('nostalgia_bin_products.json', 'r') as f:
    products = json.load(f)

# After loading the products but before insertion, convert date strings to datetime objects
print("Converting dates to datetime objects...")
for product in products:
    # Convert the date string to a datetime object
    product['date_added'] = datetime.datetime.strptime(product['date_added'], '%Y-%m-%d %H:%M:%S')

# Create embeddings for product descriptions
print("Generating OpenAI embeddings for product descriptions...")
for product in tqdm(products):
    # Generate embedding from product description
    embedding = get_embedding(product['description'])
    product['embedding'] = embedding

# Connect to Clickhouse
client = clickhouse_connect.get_client(
    host=os.getenv('CLICKHOUSE_HOST'),
    port=8443,
    username=os.getenv('CLICKHOUSE_USERNAME'),
    password=os.getenv('CLICKHOUSE_PASSWORD'),
    secure=False
)

# Create table with vector search capability
client.command('''
CREATE TABLE IF NOT EXISTS nostalgia_bin (
    product_id UInt32,
    name String,
    category String,
    subcategory String,
    era String,
    decade UInt16,
    materials Array(String),
    colors Array(String),
    condition_rating Float32,
    price_dollars Float32,
    description String,
    embedding Array(Float32),
    date_added DateTime
) ENGINE = MergeTree()
ORDER BY product_id;
''')

# Insert data
print("Inserting data into Clickhouse...")
# Convert the products to a format suitable for Clickhouse insertion
rows = []
for product in products:
    row = [
        product['product_id'],
        product['name'],
        product['category'],
        product['subcategory'],
        product['era'],
        product['decade'],
        product['materials'],
        product['colors'],
        product['condition_rating'],
        product['price_dollars'],
        product['description'],
        product['embedding'],
        product['date_added']
    ]
    rows.append(row)

# Use bulk insertion for efficiency
client.insert('nostalgia_bin', rows, 
              column_names=[
                  'product_id', 'name', 'category', 'subcategory', 'era', 
                  'decade', 'materials', 'colors', 'condition_rating', 
                  'price_dollars', 'description', 'embedding', 'date_added'
              ])

print(f"Successfully inserted {len(products)} products")

# Create a vector index for faster similarity search
client.command('''
ALTER TABLE nostalgia_bin
ADD VECTOR INDEX embedding_index embedding TYPE MSTG
GRANULARITY 1000;
''')

print("Vector index created successfully")

# Example vector search function
def vector_search(query_text, top_n=5, filter_conditions=None):
    """
    Search for products by semantic similarity with optional filtering
    
    Args:
        query_text: Text to search for
        top_n: Number of results to return
        filter_conditions: SQL WHERE clause for filtering (without the 'WHERE')
    
    Returns:
        DataFrame with search results
    """
    # Get OpenAI embedding for the query text
    query_embedding = get_embedding(query_text)
    
    # Construct the SQL query
    base_query = f'''
    SELECT 
        product_id, 
        name, 
        category,
        subcategory, 
        era, 
        decade,
        materials, 
        colors,
        condition_rating,
        price_dollars,
        description,
        L2Distance(embedding, {query_embedding}) AS distance
    FROM nostalgia_bin
    '''
    
    # Add filter conditions if provided
    if filter_conditions:
        base_query += f' WHERE {filter_conditions}'
    
    # Add ordering and limit
    base_query += f'''
    ORDER BY distance ASC
    LIMIT {top_n}
    '''
    
    # Execute the query
    result = client.query(base_query)
    
    # Convert to pandas DataFrame
    return result.to_pandas()

# Example usage
print("\nExample vector search results:")

# Search for mid-century furniture
query = "Mid-century modern furniture with clean lines and minimal design"
results = vector_search(
    query,
    top_n=3,
    filter_conditions="category = 'Furniture'"
)
print(f"\nQuery: {query}")
for _, row in results.iterrows():
    print(f"\nProduct: {row['name']}")
    print(f"Category: {row['category']} - {row['subcategory']}")
    print(f"Era: {row['era']} ({row['decade']}s)")
    print(f"Price: ${row['price_dollars']}")
    print(f"Distance: {row['distance']}")
    print(f"Description: {row['description'][:100]}...")

# Search for colorful vintage electronics
query = "Colorful retro electronics from the 80s with futuristic design"
results = vector_search(
    query,
    top_n=3,
    filter_conditions="category = 'Electronics' AND 1980 <= decade AND decade < 1990"
)
print(f"\nQuery: {query}")
for _, row in results.iterrows():
    print(f"\nProduct: {row['name']}")
    print(f"Category: {row['category']} - {row['subcategory']}")
    print(f"Era: {row['era']} ({row['decade']}s)")
    print(f"Price: ${row['price_dollars']}")
    print(f"Distance: {row['distance']}")
    print(f"Colors: {', '.join(row['colors'])}")
    print(f"Description: {row['description'][:100]}...")