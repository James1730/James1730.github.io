
const fs = require('fs');
const content = fs.readFileSync('C:\\Users\\Administrator\\Desktop\\台球桌\\sundays-website\\data\\productlist.html', 'utf8');
const match = content.match(/module-data='([^']+)'/);
if (match) {
    console.log('Module data start (encoded):', match[1].substring(0, 500));
    const decoded = decodeURIComponent(match[1]);
    console.log('Module data start (decoded):', decoded.substring(0, 500));
} else {
    console.log('No module-data found');
}
