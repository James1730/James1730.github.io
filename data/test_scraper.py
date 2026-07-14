import urllib.request
import re
import json
import time

def scrape_page(n):
    url = f"https://gzsundays.en.alibaba.com/productlist-{n}.html"
    print(f"Scraping page {n}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f"Error fetching page {n}: {e}")
        return []

    # Only look for products after "All products" or in the main list
    # In HTML, "All products" is usually a heading.
    # We can try to find the product items.
    # Products are often in a JSON-like structure in the HTML (window.renderData) or in <li> tags.
    
    products = []
    
    # Let's try to find products using regex on the HTML
    # We look for title, url, price, image
    
    # Pattern for product items in Alibaba store pages
    # <a href="//www.alibaba.com/product-detail/..." ... title="...">...</a>
    # <span class="price">...</span>
    # <img src="//s.alicdn.com/@sc04/kf/..." ...>
    
    # Actually, let's use a more general regex that catches the product-detail links
    item_matches = re.findall(r'href="(https://www\.alibaba\.com/product-detail/.*?)".*?title="(.*?)"', html)
    
    # For each match, we need price and image.
    # This might be tricky with just regex on raw HTML.
    
    # Let's try to extract the main product list part
    if 'All products' in html:
        all_products_html = html.split('All products')[1]
    else:
        all_products_html = html

    # Look for product cards
    # A typical Alibaba product card in the store:
    # <div class="product-item"> or similar
    
    # Alternative: Use the regexes I planned for the web_fetch output, 
    # but I need to get the web_fetch-like text.
    # I'll use a simple HTML-to-text conversion or just scrape specific parts.
    
    # Let's use the patterns from the prompt on the HTML if they match, 
    # or adapt them.
    
    return item_matches # Just a test

if __name__ == "__main__":
    print(scrape_page(21)[:5])
