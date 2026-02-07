import csv,random,json,logging,time,os
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def load_config():
    with open("configs/news.json", "r") as f:
        return json.load(f)

def get_page():
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    ]
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    context = browser.new_context(
        user_agent=random.choice(USER_AGENTS),
        viewport=None,
        locale="en-IN",
        timezone_id="Asia/Kolkata",
        java_script_enabled=True
    )
    return playwright, browser, context

def fetch_headlines(page,data):
    page.goto(data['url'], wait_until="domcontentloaded", timeout=90000)
    s=data['selector']
    page.wait_for_selector(s['headline'], timeout=30000)
    headlines=page.locator(s['headline']).all_inner_texts()
    time.sleep(random.uniform(2,5))
    if s['description']: 
        descriptions=page.locator(s['description']).all_inner_texts()
    else:
        descriptions=["-"]*len(headlines)
    return  list(zip(headlines,descriptions))[:12] if headlines else None


def save_to_csv(date,source,info, output_file):
    with open(output_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f,fieldnames=['date','source','headline','description'])
        if not Path(output_file).exists(): writer.writeheader()
        for i,j in info:
            writer.writerow({'date':date,'source':source,'headline':i,'description':j})

def main():
    playwright, browser, context = get_page()
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    logging.basicConfig(
    filename="logs/news_scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
     )
    logger=logging.getLogger()
    if os.path.exists(config['output_file']):
        os.remove(config['output_file'])
        logger.info(f"Existing output file {config['output_file']} removed.")
    for source in config["sources"].keys():
        page=context.new_page()
        u=config["sources"][source]
        try:
            data = fetch_headlines(page, u)
        
        except PlaywrightTimeoutError as e:
            logger.warning(f"Timeout error while scraping {source}")
            try:
              page.close()
              time.sleep(random.uniform(6,10))
              page=context.new_page()
              data = fetch_headlines(page, u)
            except PlaywrightTimeoutError:
                logger.error(f"Failed to fetch headlines from {source}")
                continue
        except Exception as e:
            logger.error(f"An error occured in {source}, {e}")
            continue
        if data:
            save_to_csv(today,source,data,config['output_file'])
            logger.info(f"Run complete from {source} with {len(data)} headlines")
        else:
                logger.warning(f"No data fetched from {source}")
        time.sleep(random.uniform(2,5))
    browser.close()
    playwright.stop()


if __name__ == "__main__":
    main() 

