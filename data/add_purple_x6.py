import json

# Product info for Purple X6
purple_x6 = {
    "name": "Luxury X6 LED Light Billiard Pool Table Customizable Logo Felt Color Premium Slate Bed Commercial Use 7FT 8FT 9FT Pool Table",
    "url": "https://www.alibaba.com/product-detail/Luxury-X6-LED-Light-Billiard-Pool_1601819353887.html",
    "price": "$1,029-1,735",
    "image": "https://sc04.alicdn.com/kf/H627a032b10034737b18757331f606d58q/Luxury-X6-LED-Light-Billiard-Pool-Table.png_480x480.jpg"
}

# 1. Load all-products-merged.json
with open(r'D:\台球桌\sundays-website\data\all-products-merged.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Check if already exists (by URL)
exists = any(p['url'] == purple_x6['url'] for p in products)

if not exists:
    # Insert at the beginning so it shows up first
    products.insert(0, purple_x6)
    print("Added Purple X6 to the catalog.")
else:
    print("Purple X6 already exists in the catalog.")

with open(r'D:\台球桌\sundays-website\data\all-products-merged.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

# 2. Recategorize (running the existing logic or just calling the update script)
# For safety, I'll just run the categorization logic here
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

for p in products:
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

# Ensure "Pool Table" category has Purple X6 at the top
# (It will be there since we inserted it at the beginning of 'products' list)

with open(r'D:\台球桌\sundays-website\data\categorized-products.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print("Categorized products updated with Purple X6.")
