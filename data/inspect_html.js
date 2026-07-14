
const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\Administrator\\Desktop\\台球桌\\sundays-website\\data\\productlist.html', 'utf8');
console.log('Content length:', content.length);
console.log('Contains "Indoor Simple Standard":', content.includes('Indoor Simple Standard'));
console.log('Contains "product-detail":', content.includes('product-detail'));

// Find first 5 occurrences of "product-detail" and show surrounding 100 chars
const index = content.indexOf('product-detail');
if (index !== -1) {
    console.log('Context around product-detail:', content.substring(index - 50, index + 150));
}
