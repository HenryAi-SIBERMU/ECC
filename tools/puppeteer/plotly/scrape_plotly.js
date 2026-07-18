const puppeteer = require('../bnpb/node_modules/puppeteer');
const fs = require('fs');

(async () => {
    console.log("Launching browser...");
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    
    // Explicitly define all categories to ensure we don't miss 3D, Subplots, Animations, etc.
    const categories = [
        { title: 'Basic Charts', url: 'https://plotly.com/python/basic-charts/' },
        { title: 'Statistical Charts', url: 'https://plotly.com/python/statistical-charts/' },
        { title: 'Scientific Charts', url: 'https://plotly.com/python/scientific-charts/' },
        { title: 'Financial Charts', url: 'https://plotly.com/python/financial-charts/' },
        { title: 'Maps', url: 'https://plotly.com/python/maps/' },
        { title: 'AI and ML', url: 'https://plotly.com/python/ai-ml/' },
        { title: 'Bioinformatics', url: 'https://plotly.com/python/bio/' },
        { title: '3D Charts', url: 'https://plotly.com/python/3d-charts/' },
        { title: 'Subplots', url: 'https://plotly.com/python/subplot-charts/' },
        { title: 'Animations', url: 'https://plotly.com/python/animations/' }
    ];
    
    // We will also scrape the main page for "Advanced" or other miscellaneous items
    categories.push({ title: 'Main Page & Advanced', url: 'https://plotly.com/python/' });

    let fullMd = '# Plotly Python Visualizations Gallery (Full Complete)\n\n';

    for (const cat of categories) {
        console.log(`Scraping category: ${cat.title} (${cat.url})`);
        try {
            await page.goto(cat.url, { waitUntil: 'networkidle2', timeout: 30000 });
            await page.waitForTimeout(2000); 
            
            const charts = await page.evaluate(() => {
                const results = [];
                const items = document.querySelectorAll('a');
                items.forEach(a => {
                    const text = a.innerText.trim().replace(/\n/g, ' ');
                    const img = a.querySelector('img'); 
                    
                    // Filter: must be a python tutorial link, not a top-level nav link, and have text
                    if (a.href.includes('/python/') 
                        && !a.href.endsWith('/python/')
                        && text 
                        && text.length > 2 
                        && text !== 'Python' 
                        && text !== 'See more'
                        && !text.includes('Plotly')) 
                    {
                        // Ensure we get absolute image URLs
                        let imgSrc = img ? img.src : null;
                        if(imgSrc && imgSrc.startsWith('/')) {
                            imgSrc = 'https://plotly.com' + imgSrc;
                        }
                        
                        results.push({ 
                            name: text, 
                            url: a.href,
                            imgSrc: imgSrc
                        });
                    }
                });
                
                const uniqueItems = [];
                const seenUrls = new Set();
                results.forEach(item => {
                    const normUrl = item.url.split('#')[0]; 
                    // Skip category index pages
                    if (!seenUrls.has(normUrl) && !normUrl.endsWith('-charts/') && !normUrl.endsWith('/maps/') && !normUrl.endsWith('/ai-ml/') && !normUrl.endsWith('/bio/')) {
                        seenUrls.add(normUrl);
                        uniqueItems.push(item);
                    }
                });
                
                return uniqueItems;
            });
            
            fullMd += `## ${cat.title}\n\n`;
            charts.forEach(chart => {
                if (chart.imgSrc) {
                    fullMd += `- [![${chart.name}](${chart.imgSrc})](${chart.url}) **[${chart.name}](${chart.url})**\n`;
                } else {
                    fullMd += `- [${chart.name}](${chart.url})\n`;
                }
            });
            fullMd += '\n';
            
        } catch (e) {
            console.log(`Failed to scrape ${cat.url}: ${e.message}`);
        }
    }

    fs.writeFileSync('plotly_gallery_deep_images.md', fullMd);
    console.log('Successfully saved full scrape to plotly_gallery_deep_images.md');
    
    await browser.close();
})();
