import urllib.request
import re
import json
import time

def scrape_store():
    all_products = {}
    
    for n in range(21, 41):
        url = f"https://gzsundays.en.alibaba.com/productlist-{n}.html"
        print(f"Scraping page {n}...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                html = response.read().decode('utf-8', 'ignore')
        except Exception as e:
            print(f"Error page {n}: {e}")
            continue
            
        # Split HTML to focus on "All products" section if possible
        if "All products" in html:
            parts = html.split("All products")
            main_content = parts[-1] # Take the last part (after "All products")
        else:
            main_content = html

        # Pattern for product items
        # We look for the link, title, price, and image.
        # Products are usually in a structured format.
        
        # A very broad regex to find product detail URLs
        # Note: In HTML, URLs often start with // or have https:
        items = re.findall(r'href="(?:https:)?(//www\.alibaba\.com/product-detail/[^"]+?\.html)"', main_content)
        # Unique list of URLs to avoid multiple hits for same product on same page
        unique_urls = []
        for it in items:
            full_url = "https:" + it if it.startswith("//") else it
            if full_url not in unique_urls:
                unique_urls.append(full_url)
        
        for p_url in unique_urls:
            # For each URL, find the title, price and image nearby in the HTML
            # We search in a window around the URL
            pos = main_content.find(p_url.replace("https:", ""))
            if pos == -1: pos = main_content.find(p_url)
            
            # Search window of 2000 chars around the link
            window = main_content[max(0, pos-1000):min(len(main_content), pos+2000)]
            
            # Find title
            title_match = re.search(r'title="(.*?)"', window)
            if not title_match:
                 # Try to find title in >Title</a>
                 title_match = re.search(r'>([^<]{10,100})</a>', window)
            
            name = title_match.group(1) if title_match else "Unknown Product"
            
            # Find price
            price_match = re.search(r'(?:\$|US\$)([\d,]+(?:-[\d,]+)?)', window)
            price = price_match.group(0) if price_match else ""
            
            # Find image
            img_match = re.search(r'src="(https://s\.alicdn\.com/@sc04/kf/[^"]+?\.(?:jpg|png|jpeg)[^"]*?)"', window)
            if not img_match:
                 img_match = re.search(r'src="(//s\.alicdn\.com/@sc04/kf/[^"]+?\.(?:jpg|png|jpeg)[^"]*?)"', window)
            
            best_img = img_match.group(1) if img_match else ""
            if best_img.startswith("//"): best_img = "https:" + best_img
            
            # Clean image URL suffix
            if best_img:
                base_img = re.sub(r'(_\d+x\d+.*?\.jpg|_\d+x\d+.*?\.png|\.jpg_.*?\.jpg)$', '.jpg', best_img)
                best_img = base_img + "_480x480.jpg"

            if p_url not in all_products:
                all_products[p_url] = {
                    "name": name,
                    "url": p_url,
                    "price": price,
                    "image": best_img
                }
        
        time.sleep(1) # Be nice
        
    return list(all_products.values())

if __name__ == "__main__":
    products = scrape_store()
    with open("products-page21-40.json", "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Total products extracted: {len(products)}")
