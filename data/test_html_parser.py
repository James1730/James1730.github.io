import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = "https://gzsundays.en.alibaba.com/productlist-1.html"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', 'ignore')
    
    decoded = urllib.parse.unquote(html).replace('\\/', '/')
    
    # Let's find all occurrences of product-detail URLs
    urls = re.findall(r'//www\.alibaba\.com/product-detail/([^"\s<>]+?\.html)', decoded)
    urls = list(set(urls))
    
    print(f"Unique URLs found: {len(urls)}")
    for u in urls[:5]:
        full_url = "https://www.alibaba.com/product-detail/" + u
        # Find window around the URL to extract name, image, price
        pos = decoded.find(u)
        window = decoded[max(0, pos-1000):min(len(decoded), pos+2000)]
        
        # In JSON, it might look like "title":"..." or "subject":"..." or "name":"..."
        # Let's search for "title":"..."
        title_match = re.search(r'"title"\s*:\s*"([^"]+?)"', window)
        if not title_match:
            title_match = re.search(r'"subject"\s*:\s*"([^"]+?)"', window)
        name = title_match.group(1) if title_match else "Unknown"
        
        price_match = re.search(r'"price"\s*:\s*"([^"]+?)"', window)
        if not price_match:
            price_match = re.search(r'(?:\$|US\$)([\d,]+(?:-[\d,]+)?)', window)
        price = price_match.group(1) if price_match else ""
        if price and not price.startswith("$"): price = "$" + price
        
        # Image
        img_match = re.search(r'"image"\s*:\s*"([^"]+?)"', window)
        if not img_match:
            img_match = re.search(r'"imgUrl"\s*:\s*"([^"]+?)"', window)
        if not img_match:
            img_match = re.search(r'(https://sc04\.alicdn\.com/kf/[^"]+?\.(?:jpg|png|jpeg))', window)
        if not img_match:
            img_match = re.search(r'(//sc04\.alicdn\.com/kf/[^"]+?\.(?:jpg|png|jpeg))', window)
            
        img = img_match.group(1) if img_match else ""
        if img.startswith("//"): img = "https:" + img
        
        print(f"URL: {full_url}")
        print(f" Name: {name}")
        print(f" Price: {price}")
        print(f" Image: {img}")
        print("-" * 40)
        
except Exception as e:
    print("Error:", e)
