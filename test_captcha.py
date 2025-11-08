from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

driver.get("https://www.target.com/p/men-s-flannel-pajama-set-goodfellow-co-black-stripe/-/A-94599750?preselect=94594593#lnk=sametab")
html = driver.page_source  # full rendered HTML

with open("bestbuy.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
