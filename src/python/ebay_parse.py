from lxml import html
import re
import csv

# Loads the HTML file
with open("../../output/pre_parsed_html/ebay.html", "r", encoding="utf-8") as f:
    doc = html.fromstring(f.read())

# this selects all product <app-item> elements
products = doc.xpath('//app-item')

data = []

for p in products:
    # Product Name
    name_el = p.xpath('.//a[contains(@href, "ebay") and normalize-space(text())]')
    name = name_el[0].text_content().strip() if name_el else "N/A"

    # Product Link
    link = name_el[0].get('href') if name_el else "N/A"

    # Product Image
    img_el = p.xpath('.//img[@src]')
    img = img_el[0].get('src') if img_el else "N/A"

    # Product Price
    price_el = p.xpath('.//div[contains(@class, "text-align-left") and contains(text(), "$") or contains(text(), "£")]/text()')
    price = price_el[0].strip() if price_el else "N/A"

    data.append((name, price, link, img))
    print(f"Product: {name}\nPrice: {price}\nLink: {link}\nImage: {img}\n{'-'*80}")

#Write to CSv
with open("ebay.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Price", "Link", "Image"])
    writer.writerows(data)

print("Scraping complete")
