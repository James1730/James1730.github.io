
const fs = require('fs');
const path = require('path');

function processFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const mapping = {};
    const matches = content.matchAll(/module-data='([^']+)'/g);
    
    for (const match of matches) {
        try {
            const decoded = decodeURIComponent(match[1]);
            const data = JSON.parse(decoded);
            
            function find(obj) {
                if (!obj || typeof obj !== 'object') return;
                
                if (Array.isArray(obj)) {
                    obj.forEach(item => {
                        if (item && item.url && item.imageUrls && item.imageUrls.original) {
                            const url = 'https:' + item.url.replace(/\\/g, '');
                            const img = 'https:' + item.imageUrls.original.replace(/\\/g, '');
                            if (url.includes('product-detail')) {
                                mapping[url] = img;
                            }
                        } else {
                            find(item);
                        }
                    });
                } else {
                    Object.values(obj).forEach(find);
                }
            }
            find(data);
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
