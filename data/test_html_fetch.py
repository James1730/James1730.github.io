import urllib.request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = "https://gzsundays.en.alibaba.com/productlist-1.html"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', 'ignore')
    print("Fetched successfully. Length:", len(html))
    print(html[:1500])
except Exception as e:
    print("Error:", e)
