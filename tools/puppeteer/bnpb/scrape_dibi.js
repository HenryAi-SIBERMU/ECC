const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const path = require('path');
const fs = require('fs');

puppeteer.use(StealthPlugin());

async function scrapeDIBI() {
    console.log('Menjalankan Puppeteer (Stealth) untuk menembus Cloudflare BNPB DIBI...');
    
    // Cari path instalasi Chrome standar di Windows
    const chromePaths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Users\\" + process.env.USERNAME + "\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
    ];
    
    let executablePath = null;
    for (const p of chromePaths) {
        if (fs.existsSync(p)) {
            executablePath = p;
            break;
        }
    }
    
    if (executablePath) {
        console.log("Menggunakan Chrome lokal pengguna:", executablePath);
    } else {
        console.log("Menggunakan Chromium bawaan Puppeteer (Bisa menyebabkan error Javascript di Superset jika versinya usang).");
    }

    const browser = await puppeteer.launch({ 
        headless: false, // Buka browser asli agar Cloudflare lebih mudah ditembus
        executablePath: executablePath,
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            '--window-size=1366,768'
        ] 
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1366, height: 768 });
    
    console.log('Mengunjungi https://dibi.bnpb.go.id/superset/dashboard/2/ ...');
    
    try {
        await page.goto('https://dibi.bnpb.go.id/superset/dashboard/2/', { waitUntil: 'networkidle2', timeout: 60000 });
        
        console.log("Menunggu 20 detik agar dasbor Superset ter-render sempurna dan melewati CAPTCHA jika ada...");
        await page.waitForTimeout(20000);
        
        const screenshotPath = path.join(__dirname, 'dibi_puppeteer_final.png');
        await page.screenshot({ path: screenshotPath, fullPage: true });
        console.log(`Screenshot halaman berhasil disimpan di: ${screenshotPath}`);
        
        console.log('Mengekstrak informasi tombol dan filter dari Superset...');
        const elementsInfo = await page.evaluate(() => {
            const getLabels = Array.from(document.querySelectorAll('label, div[role="button"], button, span.ant-select-selection-item')).map(el => ({
                text: el.innerText ? el.innerText.trim() : '',
                tag: el.tagName,
                className: el.className
            })).filter(item => item.text.length > 0 && item.text.length < 50);
            return getLabels;
        });
        
        fs.writeFileSync(path.join(__dirname, 'superset_elements_puppeteer.json'), JSON.stringify(elementsInfo, null, 2));
        console.log(`Berhasil menyimpan ${elementsInfo.length} elemen interaktif ke superset_elements_puppeteer.json`);
        
    } catch (error) {
        console.error('Terjadi kesalahan saat memuat halaman:', error);
    } finally {
        await browser.close();
    }
}

scrapeDIBI();
