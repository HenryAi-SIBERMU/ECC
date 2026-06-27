import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    print("Menjalankan Playwright untuk mengekstrak Dasbor Superset DIBI BNPB...")
    async with async_playwright() as p:
        # Buka browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1366, 'height': 768})
        page = await context.new_page()

        # Gunakan stealth untuk bypass deteksi bot
        try:
            from playwright_stealth import stealth_async
            await stealth_async(page)
        except ImportError:
            print("playwright-stealth tidak ditemukan, melanjutkan tanpa stealth.")

        print("Mengunjungi https://dibi.bnpb.go.id/ ...")
        await page.goto("https://dibi.bnpb.go.id/", wait_until="networkidle")

        print("Menunggu 15 detik agar dasbor bereaksi penuh...")
        await page.wait_for_timeout(15000)

        # Simpan screenshot
        screenshot_path = os.path.join(os.path.dirname(__file__), "dibi_playwright_screenshot.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot tersimpan di: {screenshot_path}")

        # Dapatkan semua teks
        text = await page.evaluate("document.body.innerText")
        
        # Cari elemen-elemen spesifik untuk navigasi
        print("\n--- Elemen Ditemukan ---")
        try:
            labels = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('label, div[role="button"], button')).map(el => el.innerText).filter(t => t.length > 0 && t.length < 50);
            }''')
            print("Tombol/Filter: ", labels)
        except Exception as e:
            print("Gagal mengekstrak elemen: ", e)

        with open(os.path.join(os.path.dirname(__file__), "superset_text_playwright.txt"), "w", encoding="utf-8") as f:
            f.write(text)

        print("\nTeks lengkap diekstrak dan disimpan.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
