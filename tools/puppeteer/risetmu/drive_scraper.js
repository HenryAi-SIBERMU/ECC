const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const fs = require('fs');

(async () => {
    console.log("Starting Puppeteer Drive Scraper...");
    
    // Using user data dir to use existing login
    // Note: Make sure Chrome is completely closed before running this
    const browser = await puppeteer.launch({ 
        headless: false, 
        defaultViewport: null,
        userDataDir: "C:\\Users\\yooma\\AppData\\Local\\Google\\Chrome\\User Data",
        args: ['--start-maximized']
    });
    
    const page = await browser.newPage();
    const results = {};

    const namesToSearch = ["Muhammad Fauzan Gustafi", "Amalina Nur Arifah", "Ruri Trisasri", "Adityas", "Rizal", "Wicaksono"];

    for (const name of namesToSearch) {
        // Query to search for PDFs containing the name.
        // We use type:pdf to limit it to PDF files, minimizing noise.
        const q = encodeURIComponent(`"${name}" type:pdf`);
        const searchUrl = `https://drive.google.com/drive/search?q=${q}`;
        
        console.log(`Searching for ${name}...`);
        await page.goto(searchUrl, { waitUntil: 'networkidle2' });
        
        try {
            // Wait a few seconds for the virtual DOM to render the file list
            await new Promise(r => setTimeout(r, 5000));
            
            // Try to find the first anchor tag that points to a file viewer
            const linkHref = await page.evaluate(() => {
                const anchors = Array.from(document.querySelectorAll('a[href*="/file/d/"]'));
                if (anchors.length > 0) {
                    return anchors[0].href;
                }
                
                // Fallback: search for data-id attribute anywhere in the DOM tree
                const elemWithId = document.querySelector('[data-id]');
                if (elemWithId) {
                    const id = elemWithId.getAttribute('data-id');
                    if (id && id.length > 10) {
                        return `https://drive.google.com/file/d/${id}/view`;
                    }
                }
                return null;
            });

            if (linkHref) {
                console.log(`Found link for ${name}: ${linkHref}`);
                results[name] = linkHref;
            } else {
                console.log(`Could not extract link for ${name}`);
            }
        } catch (e) {
            console.log(`Error during extraction for ${name}: ${e.message}`);
        }
    }

    fs.writeFileSync('links.json', JSON.stringify(results, null, 2));
    console.log("Saved results to links.json");
    
    await browser.close();
})();
