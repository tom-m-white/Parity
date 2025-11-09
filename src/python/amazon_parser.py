from lxml import html
import re
import csv

# Loads th e HTML file
with open("../../output/pre_parsed_html/amazon.html", "r", encoding="utf-8") as f:
    doc = html.fromstring(f.read())

# this get all product containers under the search results
#product_divs = doc.xpath('//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]')

product_divs = doc.xpath('//div[@role="listitem" and @data-asin]')
print(len(product_divs))
for div in product_divs:
    title = div.xpath('.//h2/a/span/text()')
    price = div.xpath('.//span[@class="a-price-whole"]/text()')




products = []

for div in product_divs:
    # Product link (adding Amazon domain)
    link = div.xpath('.//h2/parent::a/@href')
    link = "https://www.amazon.com" + link[0].split("?")[0] if link else None

    # Image link
    img = div.xpath('.//img[contains(@class,"s-image")]/@src')
    img = img[0] if img else None

    # Product name
    title = div.xpath('.//h2/@aria-label')
    if not title:
        title = div.xpath('.//h2//text()')
    title = title[0].strip() if title else None

    # Price (whole + fraction combined)
    whole = div.xpath('.//span[@class="a-price-whole"]/text()')
    fraction = div.xpath('.//span[@class="a-price-fraction"]/text()')
    price = None
    if whole:
        price = whole[0].strip().replace(",", "")
        if fraction:
            price += "." + fraction[0].strip()

    products.append({
        "name": title,
        "link": link,
        "image": img,
        "price": price
    })

print(f"Extracted {len(products)} products")
print(type(products))
print(type(products[0]))
for p in products[:10]:  # preview first few
    print(p)

#Write to csv
with open("amazon.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "price", "link", "image"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()       # writes: name,price,link,image
    writer.writerows(products)

print("Scraping complete")
