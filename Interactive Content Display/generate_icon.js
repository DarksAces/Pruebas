const pngToIco = require('png-to-ico');
const fs = require('fs');
const path = require('path');

// Fix for ESM/CommonJS interop
const generateIco = pngToIco.default || pngToIco;

const inputPath = path.join(__dirname, 'media_content', 'imagenes', 'icon', 'logo_256.png');
const outputPath = path.join(__dirname, 'media_content', 'imagenes', 'icon', 'logo.ico');

console.log(`Reading from: ${inputPath}`);

generateIco([inputPath])
    .then(buf => {
        fs.writeFileSync(outputPath, buf);
        console.log(`Successfully generated icon at: ${outputPath}`);
    })
    .catch(err => {
        console.error('Error generating icon:', err);
        process.exit(1);
    });
