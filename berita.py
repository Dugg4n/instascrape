from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_time_filter_code(time_range):
    # Mapping pilihan user ke parameter Google Search
    mapping = {
        "1": "qdr:h",  # 1 jam
        "2": "qdr:d",  # 1 hari
        "3": "qdr:w",  # 1 minggu
        "4": "qdr:m"   # 1 bulan
    }
    return mapping.get(time_range, "qdr:d")  # Default: 1 hari

def scrape_google_news(query, time_filter_code, max_articles=20):
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Jika ingin lihat browser, hapus baris ini
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Start WebDriver
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # Buka URL dengan filter waktu
    base_url = f"https://www.google.com/search?q={query}&tbm=nws&tbs={time_filter_code}"
    driver.get(base_url)
    time.sleep(3)

    # Ambil artikel
    articles = driver.find_elements(By.CSS_SELECTOR, "div.dbsr")[:max_articles]
    results = []

    for index, article in enumerate(articles, 1):
        try:
            title_element = article.find_element(By.TAG_NAME, "a")
            title = title_element.text.strip()
            link = title_element.get_attribute("href")
            results.append(f"{index}. {title}\n{link}\n")
        except Exception as e:
            print(f"[!] Gagal ekstrak artikel ke-{index}: {e}")

    driver.quit()

    # Simpan ke file .txt
    with open("news_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"[+] Berhasil scrap {len(results)} artikel untuk '{query}'")
    print("[+] Hasil disimpan di 'news_results.txt'")

if __name__ == "__main__":
    print("=== News Scraper Google ===")
    keyword = input("Masukkan kata kunci pencarian berita: ").strip()
    print("""
Pilih rentang waktu:
1. 1 jam terakhir
2. 24 jam terakhir
3. 7 hari terakhir
4. 1 bulan terakhir
""")
    time_range = input("Pilihan Anda (1/2/3/4): ").strip()
    time_filter_code = get_time_filter_code(time_range)
    scrape_google_news(keyword, time_filter_code)
