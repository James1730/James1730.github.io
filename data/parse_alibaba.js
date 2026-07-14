
const fs = require('fs');
const path = require('path');

function extractMapping(filePath) {
    try {
        const content = fs.readFileSync(filePath, 'utf8');
        const mapping = {};
        
        // Match anything that looks like a product URL and an image URL following it
        // Pattern: "url":"...product-detail..." ... "original":"...alicdn.com..."
        const regex = /"url":"([^"]+product-detail[^"]+)"[\s\S]{1,1000}?"original":"([^"]+alicdn\.com\/kf\/[^"]+)"/g;
        
        // Try both raw content and decoded parts
        const parts = [content];
        const moduleMatches = content.matchAll(/module-data='([^']+)'/g);
        for (const match of moduleMatches) {
            try {
                parts.push(decodeURIComponent(match[1]));
            } catch (e) {}
        }
        
        for (const part of parts) {
            let m;
            while ((m = regex.exec(part)) !== null) {
                const url = normalizeUrl(m[1]);
                const img = normalizeUrl(m[2]);
                mapping[url] = img;
            }
        }

        return mapping;
    } catch (e) {
        console.error('Error reading file:', filePath, e.message);
        return {};
    }
}

function normalizeUrl(url) {
    if (!url) return url;
    // Remove backslashes and forward slashes escapes
    url = url.replace(/\\/g, '');
    if (url.startsWith('//')) return 'https:' + url;
    return url;
}

const dir = 'C:\\Users\\Administrator\\Desktop\\台球桌\\sundays-website\\data';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let allMapping = {};
files.forEach(f => {
    const fullPath = path.join(dir, f);
    const mapping = extractMapping(fullPath);
    Object.assign(allMapping, mapping);
});

fs.writeFileSync(path.join(dir, 'alibaba-images-batch1.json'), JSON.stringify(allMapping, null, 2));
console.log(`Extracted ${Object.keys(allMapping).length} products.`);
