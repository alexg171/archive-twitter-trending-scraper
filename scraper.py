import os
import pandas as pd
import time
import argparse
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selectolax_parser import parse_with_selectolax # Ensure this filename is correct

logging.basicConfig(filename='scraper.log', level=logging.INFO)

def get_headful_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1200,800")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(options=chrome_options)

def scrape_trending_page(url, date, driver, timestamp, out_dir="out"):
    driver.get(url)
    
    try:
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.ID, "all_table")))
        
        time.sleep(1) 
        
        rendered_html = driver.page_source
        main_list, most_tweeted, longest_trending = parse_with_selectolax(rendered_html, date)
        
        if main_list and main_list[0]['Topic'] != '-':
            os.makedirs(out_dir, exist_ok=True)
            pd.DataFrame(main_list).to_csv(f"{out_dir}/trending_{timestamp}.csv", index=False, mode='a', header=not os.path.exists(f"{out_dir}/trending_{timestamp}.csv"))
            pd.DataFrame(most_tweeted).to_csv(f"{out_dir}/most_{timestamp}.csv", index=False, mode='a', header=not os.path.exists(f"{out_dir}/most_{timestamp}.csv"))
            pd.DataFrame(longest_trending).to_csv(f"{out_dir}/longest_{timestamp}.csv", index=False, mode='a', header=not os.path.exists(f"{out_dir}/longest_{timestamp}.csv"))
            logging.info(f"SUCCESS: {date.strftime('%d-%m-%Y')}")
        else:
            logging.warning(f"NO DATA: {date.strftime('%d-%m-%Y')}")

    except Exception as e:
        logging.error(f"ERROR: {date.strftime('%d-%m-%Y')}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_date", type=str, default="01-01-2019", help="Start date in MM-DD-YYYY format")
    parser.add_argument("--end_date", type=str, default="01-02-2019", help="End date in MM-DD-YYYY format")
    parser.add_argument("--region", type=str, default="united-states")
    parser.add_argument("--out_dir", type=str, default="out")
    args = parser.parse_args()

    date_range = pd.date_range(start=args.start_date, end=args.end_date)
    timestamp = int(time.time())
    
    logging.info(f"Starting scraping from {args.start_date} to {args.end_date} at timestamp {timestamp}")
    
    driver = get_headful_driver()
    
    try:
        for date in date_range:
            formatted_date = date.strftime("%d-%m-%Y")
            url = f"https://archive.twitter-trending.com/{args.region}/{formatted_date}"
            scrape_trending_page(url, date, driver, timestamp)
    finally:
        timestop = int(time.time())
        logging.info(f"Scraping completed in {timestop - timestamp} seconds.")
        driver.quit()