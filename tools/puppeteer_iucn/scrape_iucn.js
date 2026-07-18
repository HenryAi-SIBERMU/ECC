const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const path = require('path');
const fs = require('fs');

puppeteer.use(StealthPlugin());

async function scrapeIUCN() {
    console.log('Menjalankan Puppeteer (Stealth) untuk menyedot data IUCN Red List...');
    
    // Trik menggunakan Chrome asli agar tidak dicurigai bot Cloudflare IUCN
    const chromePaths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Users\\" + process.env.USERNAME + "\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"
    ];
    let executablePath = null;
    for (const p of chromePaths) {
        if (fs.existsSync(p)) { executablePath = p; break; }
    }

    const browser = await puppeteer.launch({ 
        headless: false, 
        executablePath: executablePath,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1200,800'] 
    });
    
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 800 });
    
    const speciesList = [
        "Bubalus depressicornis", // Lowland Anoa
        "Bubalus quarlesi",       // Mountain Anoa
        "Macrocephalon maleo",    // Maleo
        "Macaca nigra",           // Celebes Crested Macaque
        "Babyrousa babyrussa",    // Babirusa
        "Tarsius tarsier"         // Spectral Tarsier
    ];
    
    let results = [];

    for (const species of speciesList) {
        console.log(`\nMencari status konservasi untuk: ${species}`);
        try {
            await page.goto(`https://www.iucnredlist.org/search?query=${encodeURIComponent(species)}&searchType=species`, { waitUntil: 'networkidle2', timeout: 60000 });
            await page.waitForTimeout(10000); 
            
            const data = await page.evaluate((searchSpecies) => {
                const lines = document.body.innerText.split('\\n').map(l => l.trim()).filter(l => l.length > 0);
                
                // Cari index di mana scientific name ditemukan (case insensitive)
                const speciesIndex = lines.findIndex(l => l.toLowerCase() === searchSpecies.toLowerCase());
                
                if (speciesIndex !== -1) {
                    const commonName = lines[speciesIndex - 1]; // Baris sebelumnya biasanya nama umum
                    const populationTrend = lines[speciesIndex + 1]; // Baris setelahnya tren populasi
                    const statusRaw = lines[speciesIndex + 2]; // Baris setelahnya status (misal: "en")
                    
                    // Normalisasi kode status
                    const statusMap = {
                        'cr': 'Critically Endangered',
                        'en': 'Endangered',
                        'vu': 'Vulnerable',
                        'nt': 'Near Threatened',
                        'lc': 'Least Concern'
                    };
                    const statusText = statusMap[statusRaw.toLowerCase()] || statusRaw.toUpperCase();

                    return {
                        common_name: commonName,
                        scientific_name: lines[speciesIndex],
                        status: statusText,
                        population_trend: populationTrend
                    };
                }
                return null;
            }, species);
            
            if (data) {
                data.search_query = species;
                console.log(`Berhasil: ${data.common_name} -> ${data.status} (Populasi: ${data.population_trend})`);
                results.push(data);
            } else {
                console.log(`Gagal menemukan data untuk ${species}. Menangkap struktur teks halaman...`);
                const pageText = await page.evaluate(() => document.body.innerText);
                fs.writeFileSync(path.join(__dirname, `error_${species.replace(' ', '_')}.txt`), pageText);
            }
            
        } catch (error) {
            console.error(`Error saat memproses ${species}:`, error.message);
        }
        
        // Jeda 5 detik antar pencarian agar tidak disangka spam
        await page.waitForTimeout(5000);
    }
    
    // Simpan ke CSV
    if (results.length > 0) {
        let csvContent = "Query,Scientific Name,Common Name,Status,Population Trend\n";
        results.forEach(r => {
            csvContent += `"${r.search_query}","${r.scientific_name}","${r.common_name}","${r.status}","${r.population_trend}"\n`;
        });
        
        const outPath = path.join(__dirname, '..', '..', 'data', 'raw', 'biodiversitas_iucn_sulawesi.csv');
        fs.writeFileSync(outPath, csvContent);
        console.log(`\nSELESAI! Data biodiversitas Sulawesi berhasil diselamatkan ke: ${outPath}`);
    }
    
    await browser.close();
}

scrapeIUCN();
