import urllib.request
import urllib.parse
import re
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = "https://gzsundays.en.alibaba.com/productlist-1.html"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', 'ignore')
    
    # URL decode and replace escaped slashes
    decoded_html = urllib.parse.unquote(html).replace('\\/', '/')
    
    print("Found product-detail count in raw HTML:", len(re.findall(r'product-detail', html)))
    print("Found product-detail count in decoded HTML:", len(re.findall(r'product-detail', decoded_html)))
    
    # Try different regex patterns on decoded_html
    patterns = [
        r'"url":"([^"]+?product-detail[^"]+?)"',
        r'//www\.alibaba\.com/product-detail/[^"\s<>]+?\.html',
        r'//[a-zA-Z0-9.-]+/product-detail/[^"\s<>]+?\.html'
    ]
    
    for i, pat in enumerate(patterns, 1):
        matches = re.findall(pat, decoded_html)
        print(f"\nPattern {i} ({pat}) found {len(matches)} matches:")
        for m in matches[:10]:
            print(" -", m)
            
except Exception as e:
    print("Error:", e)
