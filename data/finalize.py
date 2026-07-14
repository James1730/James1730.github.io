import json
import os

input_file = r'C:\Users\Administrator\Desktop\台球桌\sundays-website\data\results.jsonl'
output_file = r'C:\Users\Administrator\Desktop\台球桌\sundays-website\data\products-page1-20.json'

unique_products = {}

def read_file(path):
    for enc in ['utf-8', 'utf-16', 'latin-1']:
        try:
            with open(path, 'r', encoding=enc) as f:
                return f.readlines()
        except UnicodeDecodeError:
            continue
    return []

lines = read_file(input_file)
for line in lines:
            if line.strip():
                try:
                    p = json.loads(line)
                    if p['url'] not in unique_products:
                        unique_products[p['url']] = p
                except Exception as e:
                    print(f"Error parsing line: {e}")

product_list = list(unique_products.values())

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(product_list, f, indent=2, ensure_ascii=False)

print(f"Total unique products: {len(product_list)}")
