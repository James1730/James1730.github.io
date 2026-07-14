import urllib.request
import urllib.parse
import re
import json
import time

def extract_json_object(text, pos):
    brace_count = 0
    start = -1
    for i in range(pos, -1, -1):
        if text[i] == '}':
            brace_count -= 1
        elif text[i] == '{':
            brace_count += 1
            if brace_count == 1:
                start = i
                break
                
    if start == -1:
        return None
        
    brace_count = 1
    end = -1
    for i in range(start + 1, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i
                break
                
    if end == -1:
        return None
        
    try:
        obj_str = text[start:end+1]
        return json.loads(obj_str)
    except Exception:
        return None

def scrape_pages(start_page=1, end_page=50):
    all_products = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for n in range(start_page, end_page + 1):
        url = f"https://gzsundays.en.alibaba.com/productlist-{n}.html"
        print(f"Scraping page {n} from {url}...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', 'ignore')
        except Exception as e:
            print(f"Error page {n}: {e}")
            continue
            
        decoded = urllib.parse.unquote(html).replace('\\/', '/')
        
        # Find all product-detail matches
        matches = [m.start() for m in re.finditer(r'//www\.alibaba\.com/product-detail/[^"\s<>]+?\.html', decoded)]
        print(f"Page {n}: Found {len(matches)} product-detail matches.")
        
        page_products_count = 0
        for pos in matches:
            obj = extract_json_object(decoded, pos)
            if obj:
                p_url = obj.get('url')
                if p_url:
                    if p_url.startswith("//"): p_url = "https:" + p_url
                    
                    name = obj.get('subject') or obj.get('title') or obj.get('name') or "Unknown Product"
                    name = name.strip()
                    
                    price = obj.get('fobPrice', '')
                    if "/" in price:
                        price = price.split("/")[0].strip()
                        
                    img_urls = obj.get('imageUrls', {})
                    img = img_urls.get('original') or obj.get('image') or ""
                    if img.startswith("//"): img = "https:" + img
                    
                    if img:
                        img = re.sub(r'(_\d+x\d+.*?\.jpg|_\d+x\d+.*?\.png|\.jpg_.*?\.jpg)$', '.jpg', img)
                        img = img + "_480x480.jpg"
                        
                    if name != "Unknown Product" and img:
                        all_products[p_url] = {
                            "name": name,
                            "url": p_url,
                            "price": price,
                            "image": img
                        }
                        page_products_count += 1
                        
        print(f"Page {n}: Successfully parsed {page_products_count} products.")
        time.sleep(1) # Delay to be safe
        
    return list(all_products.values())

def merge_and_categorize():
    # 1. Scrape latest products (pages 1 to 50)
    new_products = scrape_pages(1, 50)
    print(f"Scraped {len(new_products)} products from live Alibaba store.")
    
    # 2. Load existing products
    try:
        with open("data/all-products-merged.json", "r", encoding="utf-8") as f:
            existing_products = json.load(f)
    except Exception as e:
        print(f"Could not load existing merged products: {e}. Using raw fallback.")
        existing_products = []
        
    # Convert existing to dict for easy merging
    merged = {p['url']: p for p in existing_products}
    
    # Merge (new scrapes overwrite/add to existing)
    for p in new_products:
        merged[p['url']] = p
        
    # 3. Load broken images (blacklist)
    try:
        with open("data/broken-images.json", "r", encoding="utf-8") as f:
            broken = json.load(f)
            broken_urls = {item['url'] for item in broken}
    except Exception as e:
        print(f"No broken images blacklist found: {e}")
        broken_urls = set()
        
    # Filter out blacklisted or clearly broken products
    cleaned_products = []
    for url, p in merged.items():
        if url in broken_urls:
            continue
        if not p.get('image') or "Unknown" in p.get('name', ''):
            continue
        cleaned_products.append(p)
        
    # Save cleaned merged products
    with open("data/all-products-merged.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_products, f, ensure_ascii=False, indent=2)
    print(f"Merged & Cleaned catalog has {len(cleaned_products)} products.")
    
    # 4. Categorization logic
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
    
    for p in cleaned_products:
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
            
    # Clean up empty categories if any
    categories = {cat: items for cat, items in categories.items() if len(items) > 0}
            
    with open("data/categorized-products.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)
    print("Saved categorized products successfully!")

if __name__ == "__main__":
    merge_and_categorize()
