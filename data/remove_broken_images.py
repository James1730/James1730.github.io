import json

with open(r'D:\台球桌\sundays-website\data\all-products-merged.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

print(f"Original product count: {len(products)}")

# List of keywords that indicate a broken or placeholder image
BROKEN_KEYWORDS = [
    "no-photo", "no_photo", "nophoto", "placeholder", 
    "A266d87002c594a26b5fee969b9f02ec4A.png", # The Sundays logo used as fallback
    "no-image", "image-not-found"
]

cleaned = []
removed_count = 0

for p in products:
    img = p.get('image', '').lower()
    name = p.get('name', '').lower()
    
    is_broken = False
    for kw in BROKEN_KEYWORDS:
        if kw.lower() in img:
            is_broken = True
            break
            
    # Check if image URL is very short or looks like a generic Alibaba placeholder
    if not img or len(img) < 20:
        is_broken = True
        
    if is_broken:
        removed_count += 1
        continue
        
    cleaned.append(p)

print(f"Removed {removed_count} products with broken/placeholder images.")
print(f"New product count: {len(cleaned)}")

with open(r'D:\台球桌\sundays-website\data\all-products-merged.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

# Now update the categorized-products.json
categories = {
    "Multi-function Pool Table": [],
    "Glass Pool Table": [],
    "MDF Pool Table": [],
    "Snooker Table": [],
    "Chinese Billiard Table": [],
    "Coin Operated Pool Table": [],
    "Billiard Accessories": [],
    "Customized Billiard Table": [],
    "Pool Table": []
}

for p in cleaned:
    name = p.get('name', '').lower()
    if any(k in name for k in ['multi-function', 'multi function', 'multifunctional', 'dining', '3 in 1', '4 in 1', '2 in 1']):
        categories["Multi-function Pool Table"].append(p)
    elif 'glass' in name:
        categories["Glass Pool Table"].append(p)
    elif 'mdf' in name:
        categories["MDF Pool Table"].append(p)
    elif 'snooker' in name and 'chinese' not in name:
        categories["Snooker Table"].append(p)
    elif 'chinese' in name:
        categories["Chinese Billiard Table"].append(p)
    elif 'coin' in name:
        categories["Coin Operated Pool Table"].append(p)
    elif any(k in name for k in ['ball', 'cue', 'cloth', 'chalk', 'rack', 'tip', 'bridge', 'glove', 'cover', 'light', 'brush', 'triangle', 'accessori', 'felt']):
        categories["Billiard Accessories"].append(p)
    elif 'custom' in name:
        categories["Customized Billiard Table"].append(p)
    else:
        categories["Pool Table"].append(p)

# Clean up empty categories
categories = {cat: items for cat, items in categories.items() if len(items) > 0}

with open(r'D:\台球桌\sundays-website\data\categorized-products.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print("Saved updated categorized products.")
