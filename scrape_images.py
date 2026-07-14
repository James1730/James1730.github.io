"""
Batch scrape product images from Alibaba product pages.
Extracts the main product image from each page.
"""
import json
import urllib.request
import re
import time
import sys

with open('data/broken-images.json', 'r', encoding='utf-8') as f:
    broken = json.load(f)

print(f"Total products to scrape: {len(broken)}")

results = {}  # url -> image_url
failed = []

for i, item in enumerate(broken):
    url = item['url']
    if not url:
        continue
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        req.add_header('Accept-Language', 'en-US,en;q=0.9')
        
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8', errors='ignore')
        
        # Try multiple patterns to find the main product image
        img_url = None
        
        # Pattern 1: og:image meta tag (most reliable)
        m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', html)
        if m:
            img_url = m.group(1)
        
        # Pattern 2: data-role="thumb" or first product image
        if not img_url:
            m = re.search(r'"imageUrl"\s*:\s*"(https://[^"]*alicdn[^"]*\.jpg[^"]*)"', html)
            if m:
                img_url = m.group(1)
        
        # Pattern 3: any alicdn image in the product area
        if not img_url:
            m = re.search(r'(https://s\.alicdn\.com/@sc\d+/kf/[^"\'>\s]+\.jpg[^"\'>\s]*)', html)
            if m:
                img_url = m.group(1)
        
        if img_url:
            # Ensure we get 480x480 version
            if '_480x480' not in img_url and '.jpg' in img_url:
                img_url = img_url.split('.jpg')[0] + '.jpg_480x480.jpg'
            results[url] = img_url
            status = 'OK'
        else:
            results[url] = ''
            failed.append(url)
            status = 'NO IMG'
        
    except Exception as e:
        results[url] = ''
        failed.append(url)
        status = f'ERR: {str(e)[:40]}'
    
    if (i+1) % 10 == 0 or i == len(broken)-1:
        print(f"  [{i+1}/{len(broken)}] {status}")
        sys.stdout.flush()
    
    time.sleep(0.3)  # Be polite

# Save results
with open('data/scraped-images.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

found = sum(1 for v in results.values() if v)
print(f"\nDone! Found images: {found}/{len(results)}")
print(f"Failed: {len(failed)}")

if failed:
    print("\nFailed URLs:")
    for u in failed[:10]:
        print(f"  {u}")
