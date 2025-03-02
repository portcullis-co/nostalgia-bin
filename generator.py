import random
import json
import datetime
from faker import Faker
import numpy as np
from tqdm import tqdm

fake = Faker()

# Seed for reproducibility
random.seed(42)
np.random.seed(42)
fake.seed_instance(42)

# Constants
NUM_PRODUCTS = 10000
CURRENT_YEAR = 2025

# Product categories and subcategories
CATEGORIES = {
    "Furniture": ["Chairs", "Tables", "Cabinets", "Sofas", "Lamps", "Shelving", "Desks", "Dressers"],
    "Electronics": ["Audio Equipment", "Televisions", "Cameras", "Radios", "Gaming Consoles", "Computers", "Phones"],
    "Media": ["VHS Tapes", "Vinyl Records", "Cassettes", "Film Reels", "Magazines", "Books", "Posters"],
    "Fashion": ["Clothing", "Accessories", "Footwear", "Jewelry", "Watches", "Hats", "Bags"],
    "Home Decor": ["Wall Art", "Clocks", "Vases", "Mirrors", "Textiles", "Figurines", "Glassware"],
    "Collectibles": ["Toys", "Trading Cards", "Coins", "Stamps", "Memorabilia", "Action Figures", "Models"]
}

# Eras and decades
ERAS = {
    "Art Deco": [1920, 1930],
    "Mid-Century Modern": [1940, 1950, 1960],
    "Space Age": [1960, 1970],
    "Retro": [1970, 1980],
    "Vintage": [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970],
    "Classic": [1930, 1940, 1950],
    "Memphis Design": [1980],
    "Postmodern": [1980, 1990],
    "Y2K": [1990, 2000],
    "Early Digital": [1990, 2000],
    "Atomic Age": [1950],
    "Victorian": [1900, 1910],
    "Art Nouveau": [1900, 1910, 1920]
}

# Materials by category
MATERIALS = {
    "Furniture": ["Teak", "Walnut", "Oak", "Rosewood", "Glass", "Chrome", "Plastic", "Bamboo", "Rattan", "Velvet", "Leather", "Brass", "Steel", "Aluminum", "Formica"],
    "Electronics": ["Bakelite", "Plastic", "Metal", "Glass", "Wood veneer", "Chrome", "Brass", "Copper", "Rubber"],
    "Media": ["Paper", "Vinyl", "Plastic", "Magnetic Tape", "Celluloid", "Cardboard", "Film", "Glass"],
    "Fashion": ["Cotton", "Wool", "Silk", "Denim", "Leather", "Polyester", "Nylon", "Suede", "Velvet", "Cashmere", "Fur", "Rayon"],
    "Home Decor": ["Glass", "Ceramic", "Wood", "Metal", "Brass", "Silver", "Porcelain", "Textile", "Crystal", "Bronze", "Paper", "Clay"],
    "Collectibles": ["Plastic", "Die-cast Metal", "Paper", "Resin", "Vinyl", "Tin", "Glass", "Porcelain", "Cardboard", "Clay"]
}

# Colors
COLORS = [
    "Red", "Orange", "Yellow", "Green", "Blue", "Purple", "Pink", "Brown", "Black", "White", 
    "Cream", "Beige", "Gray", "Silver", "Gold", "Copper", "Bronze", "Turquoise", "Teal", "Navy", 
    "Mint", "Olive", "Maroon", "Burgundy", "Coral", "Mustard", "Amber", "Lavender", "Ivory", "Charcoal"
]

# Design styles and aesthetics by era
DESIGN_STYLES = {
    1900: ["Victorian", "Edwardian", "Art Nouveau", "Arts and Crafts"],
    1910: ["Art Nouveau", "Arts and Crafts", "Edwardian", "Early Modernism"],
    1920: ["Art Deco", "Bauhaus", "Modernism", "Jazz Age"],
    1930: ["Art Deco", "Streamline Moderne", "Modernism", "Depression Era"],
    1940: ["Mid-Century", "Utility Furniture", "Industrial", "Wartime"],
    1950: ["Mid-Century Modern", "Atomic Age", "Scandinavian", "Populuxe", "Googie"],
    1960: ["Mid-Century Modern", "Space Age", "Pop Art", "Psychedelic", "Scandinavian"],
    1970: ["Postmodern", "Disco", "Bohemian", "Earth Tones", "Brutalist"],
    1980: ["Memphis Design", "Postmodern", "New Wave", "Geometric", "Neon"],
    1990: ["Minimalism", "Grunge", "Digital Age", "Postmodern", "Retro Revival"],
    2000: ["Y2K", "Millennium", "Digital", "Minimalism", "Revival Styles"]
}

# Cultural references by decade
CULTURAL_REFS = {
    1900: ["Victorian sensibility", "Edwardian elegance", "Turn of the century", "Belle Époque"],
    1910: ["Titanic era", "World War I", "Silent film", "Ragtime"],
    1920: ["Roaring Twenties", "Jazz Age", "Prohibition", "Flappers", "Great Gatsby"],
    1930: ["Great Depression", "Hollywood Golden Age", "Art Deco", "Swing Era"],
    1940: ["World War II", "Post-war", "Big Band", "Film Noir", "Victory"],
    1950: ["Cold War", "Rock and Roll", "Elvis", "Marilyn Monroe", "American Dream"],
    1960: ["Kennedy", "Beatles", "Space Race", "Hippie", "Mod", "Woodstock"],
    1970: ["Disco", "Nixon", "Earth Day", "Star Wars", "Watergate", "ABBA"],
    1980: ["MTV", "Ronald Reagan", "New Wave", "Video Games", "Punk", "Yuppie"],
    1990: ["Grunge", "Clinton", "Internet", "Nirvana", "Hip Hop", "Friends"],
    2000: ["Y2K", "9/11", "Early Internet", "iPod", "Harry Potter", "Nokia"]
}

# Helper functions
def get_random_era():
    era = random.choice(list(ERAS.keys()))
    decade = random.choice(ERAS[era])
    return era, decade

def get_materials(category, count=None):
    if count is None:
        count = random.randint(1, 3)
    return random.sample(MATERIALS[category], min(count, len(MATERIALS[category])))

def get_colors(count=None):
    if count is None:
        count = random.randint(1, 3)
    return random.sample(COLORS, count)

def get_condition():
    # Weighted towards better condition
    conditions = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    weights = [0.01, 0.02, 0.05, 0.07, 0.15, 0.2, 0.3, 0.1, 0.1]
    return random.choices(conditions, weights=weights)[0]

def get_price(category, condition, decade):
    # Base ranges by category
    base_ranges = {
        "Furniture": (50, 2000),
        "Electronics": (30, 1000),
        "Media": (5, 200),
        "Fashion": (20, 500),
        "Home Decor": (15, 400),
        "Collectibles": (10, 1000)
    }
    
    # Calculate base price
    base_min, base_max = base_ranges[category]
    base_price = random.uniform(base_min, base_max)
    
    # Adjust by condition (better condition = higher price)
    condition_multiplier = 0.5 + (condition / 5.0)
    
    # Adjust by age/rarity (older = potentially more valuable, with some randomness)
    age = CURRENT_YEAR - decade
    age_multiplier = 1.0
    if age > 100:  # Very old pieces can be very valuable
        age_multiplier = random.uniform(1.5, 3.0)
    elif age > 70:  # Old pieces generally valuable
        age_multiplier = random.uniform(1.2, 2.0)
    elif age > 40:  # Middle-aged pieces may be valuable 
        age_multiplier = random.uniform(0.9, 1.5)
    else:  # Newer vintage items
        age_multiplier = random.uniform(0.7, 1.2)
    
    # Add a random factor for uniqueness
    unique_factor = random.uniform(0.8, 1.5)
    
    # Calculate final price
    price = base_price * condition_multiplier * age_multiplier * unique_factor
    
    # Round to a nice number
    price = round(price, -1) if price > 100 else round(price, 1)
    
    return price

def generate_name(category, subcategory, era, decade, materials):
    # Different naming patterns
    patterns = [
        f"{random.choice(DESIGN_STYLES[decade])} {subcategory.rstrip('s')}",
        f"{era} {subcategory.rstrip('s')}",
        f"{random.choice(materials)} {subcategory.rstrip('s')}",
        f"{random.choice(CULTURAL_REFS[decade])} Era {subcategory.rstrip('s')}",
        f"{decade}s {subcategory.rstrip('s')}",
        f"Vintage {subcategory.rstrip('s')}"
    ]
    
    # Choose a pattern and add some randomization
    base_name = random.choice(patterns)
    
    # Add brand or designer sometimes
    if random.random() < 0.4:
        designers = [
            fake.last_name(), 
            f"{fake.last_name()} & {fake.last_name()}",
            f"{fake.first_name()} {fake.last_name()}"
        ]
        designer = random.choice(designers)
        return f"{designer} {base_name}"
    
    # Add origin country sometimes
    if random.random() < 0.3:
        countries = ["Danish", "Swedish", "Italian", "French", "American", "Japanese", "German", "British"]
        country = random.choice(countries)
        return f"{country} {base_name}"
    
    # Add specific model or style sometimes
    if random.random() < 0.3:
        models = ["Deluxe", "Standard", "Custom", "Limited Edition", "Special", "Signature", "Premium"]
        model = random.choice(models)
        return f"{base_name} - {model} Model"
    
    return base_name

def generate_description(category, subcategory, era, decade, materials, colors, condition):
    # Start with aesthetic/stylistic description
    style_desc = random.choice([
        f"A beautiful example of {era} design.",
        f"Classic {decade}s {subcategory.lower()}.",
        f"Showcases quintessential {random.choice(DESIGN_STYLES[decade])} aesthetics.",
        f"Embodies the {era} period with its {random.choice(['clean lines', 'ornate details', 'minimalist approach', 'bold geometry'])}.",
        f"A {random.choice(['rare', 'stunning', 'pristine', 'remarkable'])} piece from the {decade}s."
    ])
    
    # Add material description
    material_list = ", ".join(materials[:-1]) + " and " + materials[-1] if len(materials) > 1 else materials[0]
    material_desc = random.choice([
        f"Crafted from {material_list}.",
        f"Made with high-quality {material_list}.",
        f"Features {material_list} construction.",
        f"Composed of {material_list}."
    ])
    
    # Add color description
    color_list = ", ".join(colors[:-1]) + " and " + colors[-1] if len(colors) > 1 else colors[0]
    color_desc = random.choice([
        f"Comes in {random.choice(['vibrant', 'rich', 'deep', 'soft', 'muted'])} {color_list}.",
        f"The {color_list} {random.choice(['tones', 'hues', 'colors', 'palette'])} {random.choice(['evoke', 'reflect', 'capture'])} the {decade}s aesthetic.",
        f"Features a {random.choice(['striking', 'classic', 'subtle', 'bold'])} {color_list} {random.choice(['finish', 'color scheme', 'palette'])}."
    ])
    
    # Add condition description
    condition_descriptions = {
        1.0: "Poor condition with significant damage, but still possesses historical value. A restoration project.",
        1.5: "Fair condition with notable wear and tear. Requires restoration.",
        2.0: "Acceptable condition with visible age-related wear. Functional but has imperfections.",
        2.5: "Moderate condition with some signs of age. Mostly functional with minor issues.",
        3.0: "Good condition for its age. Shows expected patina and minor wear.",
        3.5: "Very good condition with light signs of use. All original components intact.",
        4.0: "Excellent condition with minimal wear. Maintains original finish and functionality.",
        4.5: "Near mint condition. Minimal signs of age or use. Highly collectible state.",
        5.0: "Mint condition. Appears almost new despite its age. Museum quality piece."
    }
    condition_desc = condition_descriptions[condition]
    
    # Add cultural context
    cultural_context = random.choice([
        f"Popular during the era of {random.choice(CULTURAL_REFS[decade])}.",
        f"This piece captures the zeitgeist of {random.choice(CULTURAL_REFS[decade])}.",
        f"A nostalgic reminder of {random.choice(CULTURAL_REFS[decade])}.",
        f"Would have been found in {random.choice(['stylish homes', 'upscale apartments', 'trendy spaces', 'fashionable interiors'])} during the {decade}s."
    ])
    
    # Add emotional appeal
    emotional_appeal = random.choice([
        f"Evokes a sense of {random.choice(['nostalgia', 'history', 'timeless elegance', 'retro charm', 'vintage cool'])}.",
        f"A conversation piece that brings {random.choice(['warmth', 'character', 'history', 'charm'])} to any space.",
        f"Collectors prize these for their {random.choice(['distinctive character', 'historical significance', 'iconic design', 'nostalgic appeal'])}.",
        f"Represents a bygone era of {random.choice(['craftsmanship', 'design innovation', 'style', 'cultural expression'])}."
    ])
    
    # Combine elements with some randomization
    description_elements = [style_desc, material_desc, color_desc, condition_desc, cultural_context, emotional_appeal]
    random.shuffle(description_elements)
    
    # Add some category-specific details
    if category == "Furniture":
        furniture_details = random.choice([
            f"Features {random.choice(['tapered legs', 'curved lines', 'geometric patterns', 'organic forms', 'minimal ornamentation', 'sculptural elements'])}.",
            f"The {random.choice(['proportions', 'silhouette', 'form', 'structure'])} exemplifies {era} design philosophy.",
            f"Offers both {random.choice(['form and function', 'style and comfort', 'beauty and utility', 'aesthetics and practicality'])}."
        ])
        description_elements.append(furniture_details)
    
    elif category == "Electronics":
        electronics_details = random.choice([
            f"Still {random.choice(['functions perfectly', 'works as intended', 'operates well', 'performs admirably'])} after all these years.",
            f"Features {random.choice(['analog controls', 'vacuum tubes', 'mechanical components', 'early digital technology', 'tactile interfaces'])}.",
            f"Represents {random.choice(['early innovation', 'technological breakthroughs', 'engineering excellence', 'design evolution'])} of its time."
        ])
        description_elements.append(electronics_details)
    
    elif category == "Media":
        media_details = random.choice([
            f"Contains {random.choice(['rare recordings', 'sought-after content', 'nostalgic programming', 'classic performances', 'period-specific material'])}.",
            f"A {random.choice(['time capsule', 'cultural artifact', 'preserved memory', 'historical document'])} from the {decade}s.",
            f"Coveted by {random.choice(['collectors', 'enthusiasts', 'archivists', 'nostalgists'])} for its {random.choice(['rarity', 'content', 'condition', 'cultural significance'])}."
        ])
        description_elements.append(media_details)
    
    # Add origin information sometimes
    if random.random() < 0.4:
        origins = ["American", "Scandinavian", "Italian", "French", "German", "Japanese", "British", "Dutch"]
        origin = random.choice(origins)
        origin_desc = random.choice([
            f"Of {origin} origin.",
            f"Designed and crafted in {origin.replace('American', 'America').replace('British', 'Britain').replace('Dutch', 'the Netherlands')}.",
            f"Shows classic {origin} {random.choice(['craftsmanship', 'design sensibilities', 'aesthetics', 'influences'])}.",
            f"Part of the {origin} {random.choice(['design movement', 'artistic tradition', 'manufacturing excellence', 'creative heritage'])} of the period."
        ])
        description_elements.append(origin_desc)
    
    # Assemble final description with random length
    final_desc_length = random.randint(3, len(description_elements))
    final_description = " ".join(description_elements[:final_desc_length])
    
    return final_description

def generate_embedding():
    """Generate a mock embedding that simulates a real embedding vector"""
    # Using a dimensionality of 384 (common for many embedding models)
    vector = np.random.normal(0, 0.1, 384)
    # Normalize to unit vector (common practice for embeddings)
    vector = vector / np.linalg.norm(vector)
    return vector.tolist()

def generate_product():
    # Select category and subcategory
    category = random.choice(list(CATEGORIES.keys()))
    subcategory = random.choice(CATEGORIES[category])
    
    # Select era and decade
    era, decade = get_random_era()
    
    # Get materials, colors, condition, and price
    materials = get_materials(category)
    colors = get_colors()
    condition = get_condition()
    price = get_price(category, condition, decade)
    
    # Generate product name
    name = generate_name(category, subcategory, era, decade, materials)
    
    # Generate detailed description
    description = generate_description(category, subcategory, era, decade, materials, colors, condition)
    
    # Generate mock embedding vector
    embedding = generate_embedding()
    
    # Generate random date added (within last 3 years)
    days_ago = random.randint(0, 3 * 365)
    date_added = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    date_str = date_added.strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        "product_id": None,  # Will be assigned sequentially
        "name": name,
        "category": category,
        "subcategory": subcategory,
        "era": era,
        "decade": decade,
        "materials": materials,
        "colors": colors,
        "condition_rating": condition,
        "price_dollars": price,
        "description": description,
        "embedding": embedding,
        "date_added": date_str
    }

# Generate products
products = []
for i in tqdm(range(NUM_PRODUCTS), desc="Generating products"):
    product = generate_product()
    product["product_id"] = i + 1
    products.append(product)

# Save to JSON file
with open('nostalgia_bin_products.json', 'w') as f:
    json.dump(products, f, indent=2)

print(f"Generated {NUM_PRODUCTS} vintage products and saved to nostalgia_bin_products.json")

# Display a sample product
sample = random.choice(products)
print("\nSample Product:")
for key, value in sample.items():
    if key != "embedding":  # Skip embedding for readability
        print(f"{key}: {value}")