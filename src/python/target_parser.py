from lxml import html
import re
import csv

# Loads th e HTML file
with open("../../output/pre_parsed_html/target.html", "r", encoding="utf-8") as f:
    doc = html.fromstring(f.read())

product_divs = doc.xpath('//div[@data-test="@web/site-top-of-funnel/ProductCardWrapper"]')

products = []
print(len(product_divs))


for div in product_divs:
    # Product name
    name = div.xpath('.//a[@data-test="product-title"]/@aria-label')
    name = name[0].strip() if name else None

    # Product link
    link = div.xpath('.//a[@data-test="product-title"]/@href')
    link = "https://www.target.com" + link[0] if link else None

    # Product image
    image = div.xpath('.//img/@src')
    image = image[0] if image else None

    # Product price
    price = div.xpath('.//span[@data-test="current-price"]/span/text()')
    price = price[0].strip() if price else None

    products.append({
        "name": name,
        "price": price,
        "link": link,
        "image": image
    })

print(f"Extracted {len(products)} products.")
for p in products[:5]:
    print(p)


with open("target.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "price", "link", "image"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products)