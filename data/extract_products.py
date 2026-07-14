import re
import json
import sys

def extract_products(text):
    # Split text into pages or look for "All products" in each
    # For each page, skip "Top Picks" and focus on "All products"
    
    products = []
    
    # Simple strategy: find all product matches and images, then match them.
    # But better to stay within "All products" section.
    
    all_products_sections = re.split(r'All products', text)[1:]
    
    for section in all_products_sections:
        # Find product links and prices in the section
        # Product pattern: [Title](URL "Title")
        # Price pattern: US$NNN-NNN or $NNN-NNN
        
        # We need to find products and images in each section (page)
        # But images are at the bottom of the page (after the products list).
        
        # Let's extract all product info in this section before the next "All products" or end.
        # Product matches: (name, url)
        prod_matches = re.findall(r'\[([^\]]+)\]\((https://www\.alibaba\.com/product-detail/[^\s)]+)(?:\s+"[^"]*")?\)', section)
        
        # Prices are usually near the link. Let's try to get prices in order.
        # A more robust way: find blocks of product title + price
        # [Title](URL)
        # $Price
        
        # Let's find matches for (name, url, price)
        # We can try to look for price after the link.
        
        # Image URLs at the bottom of the page
        img_matches = re.findall(r'(https://s\.alicdn\.com/@sc04/kf/[^/\s]+\/[^/\s]+\.jpg(?:_480x480\.jpg)?)', section)
        
        for name, url in prod_matches:
            # Clean name
            name = name.strip()
            # De-duplicate by checking if product exists
            if any(p['url'] == url for p in products):
                continue
            
            # Find price near this product
            # Looking for price after the product link in the text
            price_match = re.search(re.escape(url) + r'.*?(\$|US\$)([\d,]+(?:-[\d,.]+)?(?:\s+Min\. Order:.*?)?)', section, re.DOTALL)
            price = ""
            if price_match:
                price = (price_match.group(1) + price_match.group(2)).strip()
                # Clean up "Min. Order" if it was caught
                price = re.split(r'Min\. Order', price)[0].strip()
            
            # Find image that contains keywords from product name
            # Remove symbols from name for matching
            keywords = re.sub(r'[^a-zA-Z0-9]', ' ', name).lower().split()
            # Only keep keywords > 3 chars
            keywords = [k for k in keywords if len(k) > 3]
            
            best_img = ""
            max_matches = 0
            for img_url in img_matches:
                img_lower = img_url.lower()
                matches = sum(1 for k in keywords if k in img_lower)
                if matches > max_matches:
                    max_matches = matches
                    best_img = img_url
            
            # Ensure the image is the _480x480 version as requested
            if best_img:
                if '_480x480.jpg' not in best_img:
                    # Replace suffix if it's different, or append it
                    if '.jpg' in best_img:
                        # Some URLs might have .png or other stuff but usually .jpg_480x480.jpg
                        if '.jpg_' not in best_img:
                           best_img = best_img.split('?')[0] # remove query params
                           if not best_img.endswith('_480x480.jpg'):
                               best_img = best_img + '_480x480.jpg'
                else:
                    best_img = best_img.split('?')[0]

            products.append({
                "name": name,
                "url": url,
                "price": price,
                "image": best_img
            })
            
    return products

if __name__ == "__main__":
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        content = f.read()
    
    extracted = extract_products(content)
    
    # Final de-duplication by URL just in case
    unique_products = {}
    for p in extracted:
        if p['url'] not in unique_products:
            unique_products[p['url']] = p
            
    print(json.dumps(list(unique_products.values()), indent=2))
