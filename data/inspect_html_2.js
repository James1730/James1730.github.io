
const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\Administrator\\Desktop\\台球桌\\sundays-website\\data\\productlist.html', 'utf8');
const index = content.indexOf('product-detail');
if (index !== -1) {
    const around = content.substring(index - 300, index + 1000);
    console.log('Decoded context around product-detail:');
    console.log(decodeURIComponent(around));
}
