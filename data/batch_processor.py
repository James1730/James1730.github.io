import re
import json

def extract_from_text(text):
    # This function will be customized for each batch's data
    products = []
    # Find "All products" section
    parts = text.split("All products")
    if len(parts) < 2:
        return []
    
    # Process each page in the batch
    # Each page starts with "Page URL: ..."
    pages = text.split("Page\nURL: ")
    for page in pages:
        if "All products" not in page:
            continue
        
        all_products_part = page.split("All products")[1]
        
        # Split into individual product blocks
        # Products usually followed by "Chat now"
        # Match: [Title](URL) \n Price
        items = re.findall(r'\[([^\]]+)\]\((https://www\.alibaba\.com/product-detail/[^\s)]+)(?:\s+"[^"]*")?\)\s*\n\s*(\$|US\$)([\d,.]+(?:-[\d,.]+)?(?:\s+Min\. Order:.*?)?)', all_products_part)
        
        # Images are at the bottom of the page
        # Note: web_fetch might list images at the very end of the output for the whole batch or per page.
        # In the provided output, they are at the end of each URL's section.
        img_part = page.split("Images:")[-1] if "Images:" in page else ""
        img_urls = re.findall(r'https://s\.alicdn\.com/@sc04/kf/[^/\s]+\/[^/\s]+\.jpg(?:_480x480\.jpg)?(?:\?hasNWGrade=1)?', img_part)
        
        for name, url, prefix, price_val in items:
            name = name.strip()
            price = (prefix + price_val).split("Min. Order")[0].strip()
            
            # Match image
            keywords = re.sub(r'[^a-zA-Z0-9]', ' ', name).lower().split()
            keywords = [k for k in keywords if len(k) > 3]
            best_img = ""
            max_matches = 0
            for img_url in img_urls:
                img_lower = img_url.lower()
                matches = sum(1 for k in keywords if k in img_lower)
                if matches > max_matches:
                    max_matches = matches
                    best_img = img_url
            
            if best_img:
                # Ensure _480x480 version
                best_img = best_img.split('?')[0]
                if not best_img.endswith('_480x480.jpg'):
                    if '_200x200.jpg' in best_img:
                        best_img = best_img.replace('_200x200.jpg', '_480x480.jpg')
                    elif '.jpg_' in best_img:
                         best_img = best_img.split('.jpg_')[0] + '.jpg_480x480.jpg'
                    else:
                        best_img = best_img + '_480x480.jpg'

            products.append({
                "name": name,
                "url": url,
                "price": price,
                "image": best_img
            })
    return products

# I will append the data here in the next turn
