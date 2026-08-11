/**
 * VALIDATOR: OSINT Sources URLs
 * ==============================
 * Script untuk validasi REAL semua URL di metadata JSON menggunakan Puppeteer
 * Cek apakah URL masih aktif atau 404
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

// Path ke JSON files
const JSON_FILES = [
    'data/raw/osint_logistik_pelabuhan/sources_card1_25_sumber.json',
    'data/raw/osint_logistik_pelabuhan/sources_card2_perpres_kppip.json',
    'data/raw/osint_logistik_pelabuhan/sources_card3_gni_website.json'
];

// Output report
const OUTPUT_REPORT = 'data/raw/osint_logistik_pelabuhan/URL_VALIDATION_REPORT.json';

async function checkURL(page, url, timeout = 15000) {
    try {
        const response = await page.goto(url, { 
            waitUntil: 'domcontentloaded',
            timeout: timeout 
        });
        
        const status = response.status();
        const finalURL = page.url(); // Check for redirects
        
        return {
            url: url,
            status: status,
            accessible: status >= 200 && status < 400,
            redirected: finalURL !== url,
            final_url: finalURL,
            error: null
        };
    } catch (error) {
        return {
            url: url,
            status: null,
            accessible: false,
            redirected: false,
            final_url: null,
            error: error.message
        };
    }
}

async function validateJSONFile(browser, jsonPath) {
    console.log(`\n📄 Validating: ${jsonPath}`);
    
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
    const sources = data.sources || [];
    
    const results = [];
    const page = await browser.newPage();
    
    // Set user agent to avoid blocks
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    for (const source of sources) {
        const sourceID = source.id;
        const mainURL = source.url;
        const alternativeURL = source.alternative_url;
        const archivedURL = source.archived_url;
        
        console.log(`  [${sourceID}] Checking ${source.organization || source.document_title}...`);
        
        // Check main URL
        const mainResult = await checkURL(page, mainURL);
        console.log(`    ├─ Main URL: ${mainResult.accessible ? '✅' : '❌'} (${mainResult.status || 'ERROR'})`);
        
        // Check alternative URL if exists
        let altResult = null;
        if (alternativeURL && alternativeURL !== mainURL) {
            altResult = await checkURL(page, alternativeURL);
            console.log(`    ├─ Alt URL: ${altResult.accessible ? '✅' : '❌'} (${altResult.status || 'ERROR'})`);
        }
        
        // Check archived URL if main is down
        let archiveResult = null;
        if (!mainResult.accessible && archivedURL && !archivedURL.includes('Manual download')) {
            // Try to extract real archive URL if it's a Wayback Machine pattern
            if (archivedURL.includes('web.archive.org')) {
                // Skip checking archive.org index, too generic
                console.log(`    └─ Archive URL: ⏭️  SKIPPED (generic archive.org)`);
            } else {
                archiveResult = await checkURL(page, archivedURL);
                console.log(`    └─ Archive URL: ${archiveResult.accessible ? '✅' : '❌'} (${archiveResult.status || 'ERROR'})`);
            }
        }
        
        results.push({
            source_id: sourceID,
            organization: source.organization || source.document_title,
            main_url: mainResult,
            alternative_url: altResult,
            archived_url: archiveResult,
            recommendation: getRecommendation(mainResult, altResult, archiveResult)
        });
        
        // Rate limiting
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    await page.close();
    
    return {
        file: jsonPath,
        total_sources: sources.length,
        results: results
    };
}

function getRecommendation(main, alt, archive) {
    if (main.accessible) {
        return "✅ URL utama masih aktif";
    } else if (alt && alt.accessible) {
        return "⚠️  URL utama mati, gunakan URL alternatif";
    } else if (archive && archive.accessible) {
        return "⚠️  URL utama & alternatif mati, gunakan archive";
    } else {
        return "❌ SEMUA URL MATI - Perlu dorking ulang atau ganti sumber";
    }
}

async function main() {
    console.log('🚀 Starting OSINT Sources Validation...\n');
    console.log('=' .repeat(60));
    
    const browser = await puppeteer.launch({ 
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const allResults = [];
    
    for (const jsonFile of JSON_FILES) {
        try {
            const result = await validateJSONFile(browser, jsonFile);
            allResults.push(result);
        } catch (error) {
            console.error(`❌ Error processing ${jsonFile}:`, error.message);
            allResults.push({
                file: jsonFile,
                error: error.message
            });
        }
    }
    
    await browser.close();
    
    // Generate summary
    console.log('\n' + '='.repeat(60));
    console.log('📊 VALIDATION SUMMARY\n');
    
    let totalSources = 0;
    let accessibleSources = 0;
    let deadSources = 0;
    
    allResults.forEach(fileResult => {
        if (fileResult.results) {
            console.log(`\n📁 ${path.basename(fileResult.file)}`);
            console.log(`   Total sources: ${fileResult.total_sources}`);
            
            fileResult.results.forEach(r => {
                totalSources++;
                if (r.main_url.accessible || (r.alternative_url && r.alternative_url.accessible)) {
                    accessibleSources++;
                } else {
                    deadSources++;
                    console.log(`   ❌ [${r.source_id}] ${r.organization}`);
                    console.log(`      ${r.recommendation}`);
                }
            });
        }
    });
    
    console.log('\n' + '='.repeat(60));
    console.log(`✅ Accessible: ${accessibleSources}/${totalSources} (${(accessibleSources/totalSources*100).toFixed(1)}%)`);
    console.log(`❌ Dead Links: ${deadSources}/${totalSources} (${(deadSources/totalSources*100).toFixed(1)}%)`);
    console.log('='.repeat(60));
    
    // Save report
    const report = {
        validation_date: new Date().toISOString(),
        summary: {
            total_sources: totalSources,
            accessible: accessibleSources,
            dead: deadSources,
            success_rate: (accessibleSources/totalSources*100).toFixed(2) + '%'
        },
        files: allResults
    };
    
    fs.writeFileSync(OUTPUT_REPORT, JSON.stringify(report, null, 2));
    console.log(`\n💾 Report saved: ${OUTPUT_REPORT}\n`);
}

main().catch(console.error);
