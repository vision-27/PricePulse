# FastAPI app entry point
import subprocess
import json
from fastapi import FastAPI
from pydantic import BaseModel
from database import insert_price, get_price_history
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI

app = FastAPI()
scheduler = BackgroundScheduler()
tracked_urls = {}  # {url: product_name}

class TrackRequest(BaseModel):
    url: str

def run_scraper(url):
    result = subprocess.run(["python", "scrape_runner.py", url], capture_output=True, text=True)
    try:
        output = json.loads(result.stdout)
        return output.get("title", "Title not found"), output.get("price", "Price not found")
    except json.JSONDecodeError:
        return "Title not found", "Price not found"

@app.post("/track")
def track_product(req: TrackRequest):
    url = req.url
    name, price = run_scraper(url)
    if price != "Price not found":
        insert_price(url, name, int(float(price)))
        tracked_urls[url] = name
        return {"message": f"Tracking started for {name}", "price": price}
    else:
        return {"error": "Failed to fetch price"}

@app.get("/history")
def price_history(url: str):
    return get_price_history(url)

def scheduled_scrape():
    for url, name in tracked_urls.items():
        name, price = run_scraper(url)
        if price != "Price not found":
            insert_price(url, name, int(float(price)))
            print(f"[Scheduled] Scraped {name} – ₹{price}")

scheduler.add_job(scheduled_scrape, "interval", minutes=60)
scheduler.start()
