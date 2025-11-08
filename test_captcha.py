from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

driver.get("https://www.bestbuy.com/product/samsung-65-class-s84f-oled-4k-uhd-vision-ai-smart-tizen-tv-2025/JJGRF39ZVL/sku/6643538")
html = driver.page_source  # full rendered HTML

with open("bestbuy.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
