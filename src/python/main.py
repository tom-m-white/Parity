import customtkinter as ctk
import csv
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
from lxml import html
import re

from scraper import human_get_selenium

class ParityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        #Window setup
        self.title("Parity")
        self.geometry("1500x900")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        #Top Search Frame
        self.search_frame = ctk.CTkFrame(self, corner_radius=0)
        self.search_frame.pack(fill="x", padx=20, pady=10)

        self.title_label = ctk.CTkLabel(
            self.search_frame, text="Parity", font=("Segoe UI", 28, "bold")
        )
        self.title_label.pack(pady=(10, 5))

        self.subtitle = ctk.CTkLabel(
            self.search_frame,
            text="The state or condition of being equal, especially regarding status or pay",
            font=("Segoe UI", 12), text_color="gray70"
        )
        self.subtitle.pack(pady=(0, 15))

        self.input_frame = ctk.CTkFrame(self.search_frame, corner_radius=0, fg_color="transparent")
        self.input_frame.pack(pady=(0, 10))

        self.query = ctk.StringVar()
        self.entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="Type your search here...",
            textvariable=self.query, width=350, height=40, corner_radius=10, font=("Segoe UI", 13)
        )
        self.entry.pack(side="left", padx=(0, 10))
        self.entry.bind("<Return>", self.search)

        self.search_button = ctk.CTkButton(
            self.input_frame, text="Search", width=100, height=40, corner_radius=10, command=self.search
        )
        self.search_button.pack(side="left")

        self.checkbox_frame = ctk.CTkFrame(self.search_frame, fg_color="transparent")
        self.checkbox_frame.pack(pady=(0, 15))

        # Variables to hold the state of the checkboxes (True if checked, False if not)
        self.search_ebay = ctk.BooleanVar(value=True)
        self.search_amazon = ctk.BooleanVar(value=True)
        self.search_target = ctk.BooleanVar(value=True)

        self.ebay_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text="eBay", variable=self.search_ebay,
            onvalue=True, offvalue=False
        )
        self.ebay_checkbox.pack(side="left", padx=10)

        self.amazon_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text="Amazon", variable=self.search_amazon,
            onvalue=True, offvalue=False
        )
        self.amazon_checkbox.pack(side="left", padx=10)

        self.target_checkbox = ctk.CTkCheckBox(
            self.checkbox_frame, text='Target', variable=self.search_target,
            onvalue=True, offvalue=False
        )
        self.target_checkbox.pack(side="left", padx=10)


        # Scrollable Frame for Results
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="Search Results")
        self.results_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def read_and_process_csv(self, filepath, source_name, limit=5):
        items = []
        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for i, row in enumerate(csv_reader):
                    if i >= limit:
                        break
                    row['Source'] = source_name
                    items.append(row)
        except FileNotFoundError:
            print(f"Warning: {filepath} not found. Skipping.")
        except Exception as e:
            print(f"An error occurred while reading {filepath}: {e}")
        return items

    def search(self, event=None):
        query_text = self.query.get().strip()
        if not query_text:
            return
        
        # Clear previous results and show a loading message
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        loading_label = ctk.CTkLabel(self.results_frame, text="Searching and scraping, please wait...", font=("Segoe UI", 14))
        loading_label.pack(pady=20)
        self.update_idletasks() # Force GUI to update to show the message

        # Check which boxes are ticked and run the scrapers
        sources_to_search = []
        #### EBAY ####
        if self.search_ebay.get():
            sources_to_search.append("ebay")
            human_get_selenium(query_text, "ebay", headless=True)
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
            with open("../../output/processed_csv/ebay.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Price", "Link", "Image"])
                writer.writerows(data)

            print("Scraping complete")
        #### EBAY ####

        if self.search_amazon.get():
            sources_to_search.append("amazon")
            human_get_selenium(query_text, "amazon", False)
            # Loads th e HTML file
        with open("../../output/pre_parsed_html/amazon.html", "r", encoding="utf-8") as f:
            doc = html.fromstring(f.read())

        # this get all product containers under the search results
        #product_divs = doc.xpath('//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]')

        product_divs = doc.xpath('//div[@role="listitem" and @data-asin]')

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
                "Name": title,
                "Link": link,
                "Image": img,
                "Price": price
            })

        print(f"Extracted {len(products)} products")
        print(type(products))
        print(type(products[0]))
        for p in products[:10]:  # preview first few
            print(p)

        #Write to csv
        with open("../../output/processed_csv/amazon.csv", "w", newline="", encoding="utf-8") as f:
            fieldnames = ["Name", "Price", "Link", "Image"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()       # writes: name,price,link,image
            writer.writerows(products)

        print("Scraping complete")

        if self.search_target.get():
            sources_to_search.append("target")
            human_get_selenium(query_text, "target", headless=True)
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
                    "Name": name,
                    "Price": price,
                    "Link": link,
                    "Image": image
                })

            print(f"Extracted {len(products)} products.")
            for p in products[:5]:
                print(p)


            with open("../../output/processed_csv/target.csv", "w", newline="", encoding="utf-8") as f:
                fieldnames = ["Name", "Price", "Link", "Image"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            

        # If no boxes were checked, show a message and stop
        if not sources_to_search:
            loading_label.destroy() # Remove the loading message
            no_selection_label = ctk.CTkLabel(self.results_frame, text="Please select at least one source (eBay or Amazon or Target) to search.", text_color="orange")
            no_selection_label.pack(pady=20)
            return

        # Read data from the corresponding CSVs
        all_items = []
        if "ebay" in sources_to_search:
            all_items.extend(self.read_and_process_csv('../../output/processed_csv/ebay.csv', 'eBay', limit=5))
        if "amazon" in sources_to_search:
            all_items.extend(self.read_and_process_csv('../../output/processed_csv/amazon.csv', 'Amazon', limit=5))
        if "target" in sources_to_search:
            all_items.extend(self.read_and_process_csv('../../output/processed_csv/target.csv', 'Target', limit=5))


        # Display the final results
        loading_label.destroy()
        self.display_results(all_items)

    def display_results(self, items_list):
        if not items_list:
            no_results_label = ctk.CTkLabel(self.results_frame, text="No results found from selected sources.")
            no_results_label.pack(pady=20)
            return

        for item in items_list:
            self.create_result_widget(self.results_frame, item)

    def create_result_widget(self, parent_frame, item_data):
        item_frame = ctk.CTkFrame(parent_frame, corner_radius=10)
        item_frame.pack(fill="x", padx=10, pady=10)

        img_data = None
        try:
            response = requests.get(item_data['Image'], stream=True)
            response.raise_for_status()
            pil_image = Image.open(BytesIO(response.content))
            pil_image.thumbnail((120, 120))
            img_data = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(120, 120))
        except Exception as e:
            print(f"Error processing image {item_data['Image']}: {e}")

        image_label = ctk.CTkLabel(item_frame, text="", image=img_data)
        image_label.pack(side="left", padx=10, pady=10)

        details_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        details_frame.pack(side="left", expand=True, fill="x", padx=10)

        name_label = ctk.CTkLabel(
            details_frame, text=item_data['Name'], font=("Segoe UI", 14, "bold"),
            justify="left", wraplength=550
        )
        name_label.pack(anchor="w", pady=(5, 5))

        price_label = ctk.CTkLabel(
            details_frame, text=item_data['Price'], font=("Segoe UI", 16),
            text_color="#4CAF50"
        )
        price_label.pack(anchor="w", pady=5)

        source_name = item_data.get('Source', 'Unknown')
        source_color = "#3665F3" if source_name == "eBay" else "#FF9900"

        source_label = ctk.CTkLabel(
            details_frame, text=source_name, font=("Segoe UI", 12, "bold"), text_color=source_color
        )
        source_label.pack(anchor="w", pady=(5, 0))

        link_label = ctk.CTkLabel(
            details_frame, text=f"View on {source_name}", font=("Segoe UI", 12, "underline"),
            text_color="#6495ED", cursor="hand2"
        )
        link_label.pack(anchor="w", pady=(0, 5))
        link_label.bind("<Button-1>", lambda e, url=item_data['Link']: self.open_link(url))

    def open_link(self, url):
        webbrowser.open_new_tab(url)

if __name__ == "__main__":
    app = ParityApp()
    app.mainloop()