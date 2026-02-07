📰 Multi-Site News Scraper (Playwright + Python)

"A configurable news scraping system that collects headlines and short descriptions from multiple financial/news websites and stores them in a CSV file."

Built using Python + Playwright with a modular structure so new websites can be added easily.

Features:

1.Scrapes multiple news sources in one run
2.Uses Playwright (real browser automation) to handle JavaScript-heavy sites
3.Config-driven site management (no hardcoding URLs/selectors)
4.Rotating User Agents to reduce blocking
5.Automatic CSV export
6.Logging for debugging failures per site
7.Scalable structure for adding new sites

Project Structure:

news-scraper/
│
├── main.py                # Main runner script
├── configs/
│   └── news.json          # Site configurations (URLs + selectors)
├── logs/
│   └── news_scraper.log   # Error and run logs
├── daily_news.csv         # Output file
└── README.md

⚙️ Installation
1️⃣ Clone the repo
git clone https://github.com/yourusername/news-scraper.git
cd news-scraper

2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install playwright
playwright install

How It Works:

>Reads site configurations from configs/news.json

>Opens a browser session using Playwright

>Visits each site

>Waits for content to load (including lazy loading)

>Extracts headlines + descriptions

>Appends results into daily_news.csv

>Logs success/failures in logs/news_scraper.log

Configuration (Adding/Editing Sites):

All sites are controlled from configs/news.json
Example:

{
  "sources": {
    "EconomicTimes": {
      "url": "https://economictimes.indiatimes.com/markets/stocks/news",
      "selector": {
        "container": "div.eachStory",
        "headline": "h3 a",
        "description": "p"
      }
    }
  },
  "output_file": "daily_news.csv"
}

Selector Meaning
Key	              Purpose
container	 Block containing one news item
headline	 Selector inside container for headline
description	 Selector inside container for summary (optional)

▶️ Run the Scraper
python main.py

Output will be stored in daily_news.csv

🧩 Adding a New Website

>Open the site in Chrome

>Inspect a news card

>Identify:

 1.Container element

 2.Headline element

 3.Description element (if available)

>Add selectors in news.json

>Run scraper

If it fails → check logs and adjust waits/selectors

⚠ Some modern sites load data via APIs. In that case, scraping the API directly is more stable than scraping HTML.

🐞 Troubleshooting
❌ Timeout errors

Try:

>Adding scrolling

>Increasing selector wait time

>Checking if content loads via API instead of DOM

❌ Works in browser but not Playwright

Possible reasons:

>Bot detection

>Lazy loading not triggered

>Wrong container selector

Use DevTools → Network → Fetch/XHR to check if headlines come from an API.

📌 Limitations

>Some websites use strong anti-bot protection

>Selectors may break if site layout changes

>Not designed for high-frequency scraping

⚖ Legal Note

This project is for educational purposes. Always review a website’s robots.txt and terms of service before scraping.

📈 Future Improvements

1.Proxy rotation

2.Automatic retry system

3.Email alerts

4.Database storage instead of CSV

5.API-based scraping where available

👨‍💻 Author

Built as a practical multi-site scraping framework using Playwright and Python.