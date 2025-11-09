# Parity

**Parity** is a web app built to streamline price comparison across online marketplaces like eBay and Amazon.  
It automates search queries, scrapes listings in real time using Selenium and `lxml`, and displays structured product data (including title, price, and image links) for quick comparison

> 🏆 Winner of **Best Undergraduate Project - Gonzaga Hackathon 2025**

Created by Tom White and Xavier Barinaga, Gonzaga University

---

## Features

- Automated scraping using Selenium with human-like delays to bypass captchas and gather data dynamically  
- HTML parsing to extract product information from complex DOM structures with `lxml`  
- Cross-platform search support for multiple e-commerce sites (eBay, Amazon, and more)  
- Clean data output exported as CSV files 
- Automatic photo and link extraction for each listing  
- Future goal: unified web UI for real-time price tracking and notifications  

---

## Tech Stack

| Layer | Technologies |
|-------|---------------|
| Frontend | CustomTinker |
| Backend | Python (`selenium`, `lxml`, `requests`, `re`) |
| Automation | Chrome WebDriver with custom human simulation |
| Data Storage | CSV, HTML |
| Deployment | Local (future: Docker + Flask backend) |

---
## Installation

### 1. Clone the repository

`git clone https://github.com/tomwhite/parity.git
cd parity`

### 2. Set up a virtual environment
`
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
`
### 3. Install dependencies
`pip install -r requirements.txt`

###4. Run a scraper
`python3 src/python/gui.py `

---

### Acknowledgements

Thanks to the Gonzaga Hackathon organizers, mentors, and judges for the opportunity to showcase Parity.


