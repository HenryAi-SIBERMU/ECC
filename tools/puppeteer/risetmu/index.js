require('dotenv').config();
const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const username = process.env.RISETMU_USERNAME;
const password = process.env.RISETMU_PASSWORD;
const downloadPath = process.env.DOWNLOAD_DIR || 'K:\\Shared drives\\LP2M\\1. Agenda\\2024\\12. Hibah Risetmu Batch VII';

(async () => {
    console.log("Starting Puppeteer automation...");
    const browser = await puppeteer.launch({ 
        headless: false, // Set to false so you can see it working
        defaultViewport: null,
        args: ['--start-maximized']
    });
    
    const page = await browser.newPage();
    
    // Configure download behavior to save directly to K: drive
    const client = await page.target().createCDPSession();
    await client.send('Page.setDownloadBehavior', {
        behavior: 'allow',
        downloadPath: downloadPath,
    });

    console.log("Navigating to Risetmu Login...");
    await page.goto('https://risetmu.or.id/login', { waitUntil: 'networkidle2' });

    if (username && password) {
        console.log("Filling in credentials...");
        try {
            await page.waitForSelector('input[name="username"], input[type="email"]', {timeout: 5000});
            
            const userField = await page.$('input[name="username"]') || await page.$('input[type="email"]');
            await userField.type(username);
            
            const passField = await page.$('input[name="password"]') || await page.$('input[type="password"]');
            await passField.type(password);
            
            const loginBtn = await page.$('button[type="submit"]') || await page.$('.btn-primary');
            if (loginBtn) {
                await loginBtn.click();
            } else {
                console.log("Could not find login button, please login manually.");
            }
        } catch (e) {
            console.log("Login form not found automatically, please login manually.");
        }
    } else {
        console.log("No credentials found in .env. Please login manually in the browser window.");
    }

    console.log("Waiting for dashboard to load (timeout 60s)...");
    try {
        await page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 60000 });
        console.log("Logged in successfully!");
    } catch(e) {
        console.log("Navigation wait timed out, proceeding anyway...");
    }

    const contractsUrl = 'https://risetmu.or.id/dashboard/kontrak/data?kategori=penelitian';
    console.log(`Navigating to contracts page: ${contractsUrl}`);
    await page.goto(contractsUrl, { waitUntil: 'networkidle2' });

    console.log("Extracting table rows...");
    const targetNames = ["Amalina Nur Arifah", "Muhammad Fauzan Gustafi", "Ruri Trisasri", "Adityas", "Rizal", "Wicaksono"];
    
    // Wait for the table to render
    try {
        await page.waitForSelector('table', {timeout: 10000});
        
        // This is a generic approach to find rows containing the names and click the first link/button in that row
        const rows = await page.$$('tr');
        for (const row of rows) {
            const text = await page.evaluate(el => el.innerText, row);
            for (const name of targetNames) {
                if (text.toLowerCase().includes(name.toLowerCase().split(' ')[0])) {
                    console.log(`Found row for: ${name}`);
                    // Find download button/link in this row
                    const downloadLink = await row.$('a[href*="download"], a.btn, button.btn-success, a[title*="Unduh"], a[title*="Download"]');
                    if (downloadLink) {
                        console.log(`Clicking download for ${name}...`);
                        await downloadLink.click();
                        await new Promise(r => setTimeout(r, 3000)); // wait for download to start
                    } else {
                        console.log(`Could not find download button in row for ${name}`);
                    }
                }
            }
        }
    } catch (e) {
        console.log("Table not found or error parsing rows:", e.message);
    }

    console.log("Automation complete. Browser will remain open for 60 seconds to ensure downloads finish.");
    await new Promise(r => setTimeout(r, 60000));
    await browser.close();
})();
