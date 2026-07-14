
const fs = require('fs');
const path = require('path');

function processFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const mapping = {};
    const matches = content.matchAll(/module-data='([^']+)'/g);
    
    for (const match of matches) {
        try {
            const decoded = decodeURIComponent(match[1]);
            if (decoded.includes('product-detail')) {
                // This is likely a product list module
                // Use a very loose regex to find url and image pairs
                const regex = /"url":"([^"]+product-detail[^"]+)"[^}]+?"original":"([^"]+alicdn\.com\/kf\/[^"]+)"/g;
                let m;
                while ((m = regex.exec(decoded)) !== null) {
                    const url = 'https:' + m[1].replace(/\\/g, '');
                    const img = 'https:' + m[2].replace(/\\/g, '');
                    mapping[url] = img;
                }
            }
        } catch (e) {}
    }
    return mapping;
}

const dir = 'C:\\Users\\Administrator\\Desktop\\台球桌\\sundays-website\\data';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let allMapping = {};
files.forEach(f => {
    const m = processFile(path.join(dir, f));
    Object.assign(allMapping, m);
});

fs.writeFileSync(path.join(dir, 'alibaba-images-batch1.json'), JSON.stringify(allMapping, null, 2));
console.log(`Extracted ${Object.keys(allMapping).length} products.`);
