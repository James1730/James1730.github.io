
const fs = require('fs');
const path = require('path');

function extract(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const mapping = {};
    
    // Extract anything that looks like a product URL and an image URL
    // We'll just look for all of them and try to associate them by vicinity
    const items = content.split('product-detail');
    for (let i = 1; i < items.length; i++) {
        const item = items[i];
        // The URL is before 'product-detail' and after it.
        // Let's find the ID and construct the URL
        const idMatch = item.match(/_(\d+)\.html/);
        if (idMatch) {
            const id = idMatch[1];
            // Find the first alicdn.com/kf image in this block
            const imgMatch = item.match(/alicdn\.com\/kf\/([^\.]+)\.([a-z]+)/);
            if (imgMatch) {
                const imgUrl = 'https://sc04.alicdn.com/kf/' + imgMatch[1] + '.' + imgMatch[2];
                // Construct product URL (need some slug, or just use the ID)
                // Actually, let's try to find the whole URL in the previous chunk
                const prev = items[i-1];
                const urlMatch = prev.match(/\/\/[^"]+$/);
                if (urlMatch) {
                    const url = 'https:' + urlMatch[0] + 'product-detail' + item.substring(0, item.indexOf('.html') + 5).replace(/\\/g, '');
                    mapping[url] = imgUrl;
                }
            }
        }
    }
    return mapping;
}

const dir = 'C:\\Users\\Administrator\\Desktop\\台球桌\\sundays-website\\data';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let allMapping = {};
files.forEach(f => {
    const mapping = extract(path.join(dir, f));
    Object.assign(allMapping, mapping);
});

fs.writeFileSync(path.join(dir, 'alibaba-images-batch1.json'), JSON.stringify(allMapping, null, 2));
console.log(`Extracted ${Object.keys(allMapping).length} products.`);
