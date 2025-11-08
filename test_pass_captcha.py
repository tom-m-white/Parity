import requests, random, time
import random

def human_get(url, session=None, headers=None, min_delay=1.5, max_delay=4.0, timeout=10):
    if session is None:
        session = requests.Session()
    if headers is None:
        headers = {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
        ])}

    response = session.get(url, headers=headers, timeout=timeout)
    delay = random.uniform(min_delay, max_delay)
    print(f"[{response.status_code}] Sleeping for {delay:.2f}s")
    time.sleep(delay)
    return response

HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/121.0.6167.85 Safari/537.36"},
]
url = "https://www.amazon.com/s?k=turntable"

headers = random.choice(HEADERS_LIST)

response = human_get(url, headers=headers)
html = response.text
with open("amazon.html", "w", encoding="utf-8") as f:
    f.write(html)

def human_get(url, session=None, headers=None, min_delay=1.5, max_delay=4.0, timeout=10):
    if session is None:
        session = requests.Session()
    if headers is None:
        headers = {"User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"
        ])}

    response = session.get(url, headers=headers, timeout=timeout)
    delay = random.uniform(min_delay, max_delay)
    print(f"[{response.status_code}] Sleeping for {delay:.2f}s")
    time.sleep(delay)
    return response