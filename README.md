# PricePulse
A product price tracker for Amazon and other E-Commerce websites.

After researching about web scrapers, and ease of integration with a python-based environment, here's an overview:
| Tool          | Pros                             | Cons                                |
| --------------| -------------------------------- | ----------------------------------- |
| Selenium      | Handles JavaScript-heavy pages   | Slower, requires browser            |
| Playwright    | Fast headless browser automation | Slightly complex setup              |
| BeautifulSoup | Simple for static pages          | May not work if JS rendering needed |

I am using Playright with python, as it is fast and works well with dynamic content

The tech stack I plan to use is:

  Frontend: HTML + JS + Chart.js (JavaScript to fetch price data and update the UI dynamically, Chart.js to plot the price trend graph)
  
  Backend: Python + FastAPI
  
  Database: SQLite
  
  Scraper: Playwright (Python)
  
  Scheduler: APScheduler (Python based, easier integration)
  
  Deployment: Render (backend) + Vercel (frontend)
