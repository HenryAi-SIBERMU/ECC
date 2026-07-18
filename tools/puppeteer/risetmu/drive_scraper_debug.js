const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const fs = require('fs');

(async () => {
    console.log("Starting Puppeteer Drive Scraper for Debugging...");
    const browser = await puppeteer.launch({ 
        headless: false, 
        defaultViewport: null,
        userDataDir: "C:\\Users\\yooma\\AppData\\Local\\Google\\Chrome\\User Data",
        args: ['--start-maximized']
    });
    
    const page = await browser.newPage();
    const name = "Muhammad Fauzan Gustafi";
    
    const q = encodeURIComponent(`"${name}" type:pdf`);
    const searchUrl = `https://drive.google.com/drive/search?q=${q}`;
    
    console.log(`Searching for ${name}...`);
    await page.goto(searchUrl, { waitUntil: 'networkidle2' });
    
    await new Promise(r => setTimeout(r, 10000));
    
    await page.screenshot({ path: 'debug_drive.png' });
    const html = await page.content();
    fs.writeFileSync('debug_drive.html', html);
    
    console.log("Saved debug_drive.png and debug_drive.html");
    await browser.close();
})();
