from lxml import html
import re

# Loads th e HTML file
with open("../../output/pre_parsed_html/ebay.html", "r", encoding="utf-8") as f:
    doc = html.fromstring(f.read())

# this get all product containers under the search results
product_divs = doc.xpath('//*[@id="mainContent"]/div[2]/div/div/div/div[@class="app-item" or starts-with(name(), "app-item") or descendant::app-item]')

if not product_divs:
    product_divs = doc.xpath('//*[@id="mainContent"]/div[2]/div/div/div/div[contains(@class, "col-lg-") and descendant::div[contains(text(), "$")]]')

# this does it for each listing
for div in product_divs:
    
    text = " ".join(div.xpath('.//text()')).strip()
    text = re.sub(r'\s+', ' ', text)

    name = re.split(r'Seller:|Price', text)[0].strip()

    price_elements = div.xpath('.//div[contains(@class, "text-align-left") and contains(text(), "$")]/text()')
    price = price_elements[0].strip() if price_elements else "N/A"

    print(f"Product: {name} | Price: {price}")
