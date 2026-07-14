import re
import json
import sys

def extract_products(text):
    products = []
    # Find "All products" section(s)
    # The text might contain multiple pages, each with its own "All products" section
    pages = text.split("Page URL: ")
    for page in pages:
        if "All products" not in page:
            continue
        
        all_products_part = page.split("All products")[1]
        # Further split to avoid "Get support" and other footer stuff
        all_products_part = all_products_part.split("Get support")[0]
        
        # Pattern for product links and titles
        # [Title](URL)
        prod_pattern = re.compile(r'\[([^\]]+)\]\((https://www\.alibaba\.com/product-detail/[^\s)]+)(?:\s+"[^"]*")?\)')
        
        # Prices usually follow the link
        # Look for the next price after each product link
        matches = list(prod_pattern.finditer(all_products_part))
        
        # Extract images from the same page (they are listed at the bottom of the page section)
        img_pattern = re.compile(r'https://s\.alicdn\.com/@sc04/kf/[^/\s]+\/[^/\s]+\.jpg(?:_480x480\.jpg)?(?:\?hasNWGrade=1)?')
        img_urls = img_pattern.findall(page)
        
        for i, match in enumerate(matches):
            name = match.group(1).strip()
            url = match.group(2).strip()
            
            # Find price between this product and the next one
            start = match.end()
            end = matches[i+1].start() if i+1 < len(matches) else len(all_products_part)
            chunk = all_products_part[start:end]
            
            price_match = re.search(r'(\$|US\$)([\d,.]+(?:-[\d,.]+)?(?:\s+Min\. Order:.*?)?)', chunk)
            price = ""
            if price_match:
                price = (price_match.group(1) + price_match.group(2)).split("Min. Order")[0].strip()
            
            # Match image
            keywords = re.sub(r'[^a-zA-Z0-9]', ' ', name).lower().split()
            keywords = [k for k in keywords if len(k) > 3]
            best_img = ""
            max_matches = 0
            for img_url in img_urls:
                img_lower = img_url.lower()
                # Check for keyword matches in the filename part of the URL
                filename = img_url.split('/')[-1].lower()
                m = sum(1 for k in keywords if k in filename)
                if m > max_matches:
                    max_matches = m
                    best_img = img_url
            
            if best_img:
                best_img = best_img.split('?')[0]
                if not best_img.endswith('_480x480.jpg'):
                    if '_200x200.jpg' in best_img:
                        best_img = best_img.replace('_200x200.jpg', '_480x480.jpg')
                    elif '.jpg_' in best_img:
                         best_img = best_img.split('.jpg_')[0] + '.jpg_480x480.jpg'
                    else:
                        best_img = best_img + '_480x480.jpg'
                else:
                    # Already ends with _480x480.jpg, but might have been double extension
                    if best_img.endswith('.jpg_480x480.jpg'):
                        pass # correct
            
            products.append({
                "name": name,
                "url": url,
                "price": price,
                "image": best_img
            })
    return products

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = f.read()
    results = extract_products(data)
    for r in results:
        print(json.dumps(r))
