# Store Scraper (Shopify Stores Only)

This is a Selenium-based scraping script that:

- Downloads all products from a shopify store
- Searches for specific perfume names across multiple pages
- Matches products using custom logic
- Downloads and resizes product images
- Extracts and adjusts prices

## How it works

1. Loads a list of product names from a JSON file
2. Iterates through multiple pages of a website
3. Matches products based on name
4. Downloads images and saves them locally

## Tech used

- Python
- Selenium
- Requests
- Pillow (PIL)

## Note

- This project was built for a specific use case and is not optimized for general use.
its worflow is as follows:
  - run scraper.py
  - run downloadjson.py
  - run searcher.py
  - run scraper2.py