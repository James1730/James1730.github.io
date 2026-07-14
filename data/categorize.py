import json, re

with open(r'C:\Users\Administrator\Desktop\台球桌\sundays-website\data\all-products-merged.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

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

total = 0
for cat, items in categories.items():
    print(f'{cat}: {len(items)}')
    total += len(items)
print(f'Total: {total}')

with open(r'C:\Users\Administrator\Desktop\台球桌\sundays-website\data\categorized-products.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)
print('Saved to categorized-products.json')
