# Scraper logic

from playwright.sync_api import sync_playwright
import re

def scrape_amazon_product(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Setting a realistic user agent and viewport
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        page.set_viewport_size({"width": 1280, "height": 720})
        
        title = "Title not found"
        price = "Price not found"
        
        try:
            page.goto(url, timeout=60000)
            
            # using a more specific selector for getting a title
            title_selector = 'span#productTitle.a-size-large'
            if page.locator(title_selector).count() > 0:
                title = page.locator(title_selector).first.text_content().strip()
            else:
                # if span not found, fallback to hidden input field
                hidden_title = page.locator('input#productTitle[type="hidden"]').first.get_attribute('value')
                if hidden_title:
                    title = hidden_title.strip()
        
            # Try multiple price selectors - based on Amazon's different layouts
            price_selectors = [
                'span.a-price-whole',                      # Standard product page
                'span.a-offscreen',                        # Sometimes price is here
                'span.priceToPay span.a-price-whole',     # Deal price
                'span.apexPriceToPay span.a-price-whole', # Another variation
                'span.a-price[data-a-size="xl"] span'    # Sometimes in this structure
            ]
            
            for selector in price_selectors:
                if page.locator(selector).count() > 0:
                    price_text = page.locator(selector).first.text_content().strip()
                    price = re.sub(r'[^\d.]', '', price_text)  # Keeping digits and decimal
                    break
                    
            return title, price
            
        except Exception as e:
            print(f"Error scraping product: {str(e)}")
            return title, price
            
        finally:
            browser.close()
