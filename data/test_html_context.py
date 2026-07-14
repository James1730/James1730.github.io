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
    
    decoded = urllib.parse.unquote(html).replace('\\/', '/')
    
    # Let's find one product URL
    u = "Modern-LED-Pool-Table-Custom-Logo_1601819327897.html"
    pos = decoded.find(u)
    if pos != -1:
        print("FOUND URL at pos:", pos)
        print("CONTEXT:")
        print(decoded[pos-800:pos+800])
    else:
        print("NOT FOUND")
        
except Exception as e:
    print("Error:", e)
