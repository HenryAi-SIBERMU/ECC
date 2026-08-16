const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');

puppeteer.use(StealthPlugin());

const PDF_DIR = path.join('c:', 'Users', 'yooma', 'OneDrive', 'Desktop', 'duniahub', 'client', '4. Celios2', 'data', 'raw', 'osint_logistik_pelabuhan', 'pdf');
const SCREENSHOT_DIR = path.join('c:', 'Users', 'yooma', 'OneDrive', 'Desktop', 'duniahub', 'client', '4. Celios2', 'data', 'raw', 'osint_logistik_pelabuhan', 'screenshots');

(async () => {
    console.log('=== ROUND FINAL: Vale Sustainability PDF + GNI AMDAL sources ===');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });

    // ======== 1. Vale Sustainability Report - click download button directly ========
    console.log('\n[1] Vale Documents page - find and click Sustainability Report download...');
    try {
        const page = await browser.newPage();
        const client = await page.target().createCDPSession();
        await client.send('Page.setDownloadBehavior', { behavior: 'allow', downloadPath: PDF_DIR });
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0');

        await page.goto('https://www.vale.com/indonesia/documents-and-reports', { waitUntil: 'networkidle2', timeout: 30000 });
        await new Promise(r => setTimeout(r, 3000));
        console.log(`  Page: ${await page.title()}`);

        // Get all PDF links with their full URLs including those with token
        const pdfLinks = await page.evaluate(() => {
            return Array.from(document.querySelectorAll('a[href]'))
                .map(a => ({ text: a.innerText.trim().substring(0,100), href: a.href }))
                .filter(l => l.href && l.href.includes('.pdf') &&
                    (l.href.toLowerCase().includes('sustain') || l.href.toLowerCase().includes('annual') ||
                     l.text.toLowerCase().includes('sustain') || l.text.toLowerCase().includes('annual') ||
                     l.text.toLowerCase().includes('laporan tahunan')));
        });
        console.log(`  Sustainability/Annual PDF links: ${JSON.stringify(pdfLinks, null, 2)}`);

        // Navigate to the Sustainability Report 2025 URL found earlier, with ?download=true
        const sustainUrl = 'https://www.vale.com/documents/44618/1373270/PT+Vale+Indonesia+Tbk+-+Sustainabilty+Report+2025+-+English.pdf/1373270?version=1.0&t=1771916505583&download=true';
        
        // Intercept PDF response
        page.on('response', async resp => {
            const ct = resp.headers()['content-type'] || '';
            const url = resp.url();
            if ((ct.includes('pdf') || ct.includes('octet')) && !url.includes('linkedin') && !url.includes('google')) {
                try {
                    const buf = await resp.buffer();
                    if (buf && buf.slice(0,4).toString() === '%PDF') {
                        const dest = path.join(PDF_DIR, 'Vale_Sustainability_Report_2025_ORIGINAL.pdf');
                        fs.writeFileSync(dest, buf);
                        console.log(`  SAVED Vale Sustainability: ${dest} (${buf.length} bytes)`);
                    }
                } catch(e) {}
            }
        });

        // Try clicking the Sustainability Report link directly
        const sustainBtn = await page.$('a[href*="Sustainabilty+Report"]');
        if (sustainBtn) {
            console.log('  Found Sustainability Report link, clicking...');
            await sustainBtn.click();
            await new Promise(r => setTimeout(r, 8000));
        }

        // Check what files exist now
        const files = fs.readdirSync(PDF_DIR).filter(f => f.toLowerCase().includes('vale') || f.toLowerCase().includes('sustain'));
        console.log(`  Vale/Sustain files: ${files}`);
        await page.close();
    } catch(e) {
        console.log(`  [VALE ERROR] ${e.message}`);
    }

    // ======== 2. Find GNI AMDAL/IUP official document ========
    console.log('\n[2] Searching for GNI official AMDAL/permit document...');
    const gniUrls = [
        // KLHK AMDAL database
        'https://amdal.menlhk.go.id/',
        // Kemenperin IUI database  
        'https://peraturan.go.id/',
        // OSS perizinan
        'https://oss.go.id/',
        // Try GNI direct website
        'https://gunbusternickelindustry.com',
        'https://www.gni.co.id',
    ];

    try {
        const page = await browser.newPage();
        await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0');
        const client = await page.target().createCDPSession();
        await client.send('Page.setDownloadBehavior', { behavior: 'allow', downloadPath: PDF_DIR });

        for (const url of gniUrls) {
            try {
                console.log(`  Trying: ${url}`);
                const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
                const title = await page.title();
                console.log(`  Status: ${resp.status()} | Title: ${title}`);
                await page.screenshot({ path: path.join(SCREENSHOT_DIR, `gni_${url.replace(/https?:\/\//,'').replace(/\//g,'_')}.png`) });

                const pdfLinks = await page.evaluate(() =>
                    Array.from(document.querySelectorAll('a[href]'))
                        .map(a => ({ text: a.innerText.trim().substring(0,80), href: a.href }))
                        .filter(l => l.href && (l.href.includes('.pdf') || l.text.toLowerCase().includes('amdal') || l.text.toLowerCase().includes('permit')))
                );
                if (pdfLinks.length) console.log(`  PDF Links: ${JSON.stringify(pdfLinks.slice(0,5), null, 2)}`);
            } catch(e) {
                console.log(`  ERR: ${e.message.substring(0,80)}`);
            }
        }
        await page.close();
    } catch(e) {
        console.log(`  [GNI ERROR] ${e.message}`);
    }

    await browser.close();
    console.log('\n=== FINAL PDF DIR (valid only) ===');
    fs.readdirSync(PDF_DIR).forEach(f => {
        const fpath = path.join(PDF_DIR, f);
        const size = fs.statSync(fpath).size;
        if (size < 10000) return; // skip tiny files
        const buf = Buffer.alloc(5);
        const fd = fs.openSync(fpath, 'r');
        fs.readSync(fd, buf, 0, 5, 0);
        fs.closeSync(fd);
        if (buf.slice(0,4).toString() === '%PDF')
            console.log(`  [OK] ${f} (${(size/1024/1024).toFixed(2)} MB)`);
    });
})();
