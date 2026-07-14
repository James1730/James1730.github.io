import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
url = "https://gzsundays.en.alibaba.com/productlist-1.html"

def extract_json_object(text, pos):
    # Find start of JSON object (enclosing brace { before pos)
    brace_count = 0
    start = -1
    for i in range(pos, -1, -1):
        if text[i] == '}':
            brace_count -= 1
        elif text[i] == '{':
            brace_count += 1
            if brace_count == 1:
                start = i
                break
                
    if start == -1:
        return None
        
    # Find end of JSON object (balanced brace } after pos)
    brace_count = 1
    end = -1
    for i in range(start + 1, len(text)):
        if text[i] == '{':
            brace_count += 1
        elif text[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                end = i
                break
                
    if end == -1:
        return None
        
    try:
        obj_str = text[start:end+1]
        return json.loads(obj_str)
    except Exception as e:
        # If it fails, maybe there are nested strings or Escaped quotes, let's try a loose parse
        # or clean up. But often direct loads works if we balanced properly.
        return None

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8', 'ignore')
    
    decoded = urllib.parse.unquote(html).replace('\\/', '/')
    
    # Find all product-detail matches
    matches = [m.start() for m in re.finditer(r'//www\.alibaba\.com/product-detail/[^"\s<>]+?\.html', decoded)]
    print(f"Total product-detail positions: {len(matches)}")
    
    parsed_count = 0
    for pos in matches:
        obj = extract_json_object(decoded, pos)
        if obj:
            parsed_count += 1
            print(f"Product {parsed_count}:")
            print("  URL:", obj.get('url'))
            # Print all possible keys to inspect
            print("  Subject/Title:", obj.get('subject') or obj.get('title') or obj.get('name'))
            print("  Price (fobPrice):", obj.get('fobPrice'))
            img_urls = obj.get('imageUrls', {})
            print("  Image (original):", img_urls.get('original') or obj.get('image'))
            print("-" * 50)
            
    print(f"Successfully parsed {parsed_count} out of {len(matches)} products using balanced brace JSON parser.")
except Exception as e:
    print("Error:", e)
