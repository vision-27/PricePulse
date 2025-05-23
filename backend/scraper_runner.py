# scrape_runner.py
from playwright.sync_api import sync_playwright
import sys
import re
import json

def scrape(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        page.set_viewport_size({"width": 1280, "height": 720})

        title = "Title not found"
        price = "Price not found"

        try:
            page.goto(url, timeout=60000)

            if page.locator('span#productTitle.a-size-large').count() > 0:
                title = page.locator('span#productTitle.a-size-large').first.text_content().strip()
            else:
                hidden_title = page.locator('input#productTitle[type="hidden"]').first.get_attribute('value')
                if hidden_title:
                    title = hidden_title.strip()

            price_selectors = [
                'span.a-price-whole',
                'span.a-offscreen',
                'span.priceToPay span.a-price-whole',
                'span.apexPriceToPay span.a-price-whole',
                'span.a-price[data-a-size="xl"] span'
            ]

            for selector in price_selectors:
                if page.locator(selector).count() > 0:
                    price_text = page.locator(selector).first.text_content().strip()
                    price = re.sub(r'[^\d.]', '', price_text)
                    break

        except Exception as e:
            print(json.dumps({"error": str(e)}))
            return

        finally:
            browser.close()

        result = {"title": title, "price": price}
        print(json.dumps(result)) 

if __name__ == "__main__":
    url = sys.argv[1]
    scrape(url)
