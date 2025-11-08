import requests, random, time
import random
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def human_get_selenium():
    options = Options()
    options.add_argument(
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.105 Mobile Safari/537.36"
    )
    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    #options.add_argument("--enable-javascript")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_argument("--headless")
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    # driver = webdriver.Chrome(options=options)
    encoded_query = "bike"
    driver.get(f"https://globalesearch.com/search/shoes?sortBy=BestMatch&searchInDescription=false&se=0")
    html = driver.page_source  # full rendered HTML

    soup = BeautifulSoup(html, "html.parser")
    pretty_html = soup.prettify()

    with open("ebay.html", "w", encoding="utf-8") as f:
        f.write(pretty_html)

    driver.quit()

def human_get_selenium_wait():
    options = Options()
    options.add_argument(
        "Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.105 Mobile Safari/537.36"
    )
    # Adding argument to disable the AutomationControlled flag
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Exclude the collection of enable-automation switches
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Turn-off userAutomationExtension
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    #options.add_argument("--enable-javascript")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    #options.add_argument("--headless")
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    options.add_argument("--disable-gpu")

    encoded_query = "bike"
    driver.get(f"https://globalesearch.com/search/shoes?sortBy=BestMatch&searchInDescription=false&se=0")

    time.sleep(5)

    html = driver.page_source  # full rendered HTML

    soup = BeautifulSoup(html, "html.parser")
    pretty_html = soup.prettify()

    with open("ebay.html", "w", encoding="utf-8") as f:
        f.write(pretty_html)

    input("Press Enter to close browser...")

    driver.quit()

def human_get_requests(url, session=None, headers=None, min_delay=1.5, max_delay=4.0, timeout=10):
    if session is None:
        session = requests.Session()
    if headers is None:
        headers = {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/121.0.6167.85 Safari/537.36"
        ])}

    response = session.get(url, headers=headers, timeout=timeout)
    delay = random.uniform(min_delay, max_delay)
    print(f"[{response.status_code}] Sleeping for {delay:.2f}s")
    time.sleep(delay)
    return response



# url = "https://globalesearch.com"

# response = human_get_requests(url)
# html = response.text
# soup = BeautifulSoup(html, "html.parser")
# pretty_html = soup.prettify()
# with open("ebay.html", "w", encoding="utf-8") as f:
#     f.write(pretty_html)

# human_get_selenium()

human_get_selenium_wait()
