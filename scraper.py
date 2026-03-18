import os
import pandas as pd
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selectolax_parser import parse_with_selectolax

def scrape_trending_page(url, date, driver, timestamp):
    driver.get(url)
    print(f"Waiting 10 seconds for JS to load...")
    time.sleep(10) 
    
    rendered_html = driver.page_source
    main_list, most_tweeted, longest_trending = parse_with_selectolax(rendered_html, date)
    
    pd.DataFrame(main_list).to_csv(f"out/trending_table_data_{timestamp}.csv", index=False, mode='a', header=not os.path.exists(f"trending_table_data_{timestamp}.csv"))
    pd.DataFrame(most_tweeted).to_csv(f"out/most_tweeted_data_{timestamp}.csv", index=False, mode='a', header=not os.path.exists(f"most_tweeted_data_{timestamp}.csv"))
    pd.DataFrame(longest_trending).to_csv(f"out/longest_trending_data_{timestamp}.csv", index=False, mode='a', header=not os.path.exists(f"longest_trending_data_{timestamp}.csv"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_date", type=str, default="01-01-2019")
    parser.add_argument("--end_date", type=str, default="01-02-2019")
    args = parser.parse_args()

    date_range = pd.date_range(start=args.start_date, end=args.end_date)
        
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0...")

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        timestamp = time.time()
        for date in date_range:
            formatted_date = date.strftime("%d-%m-%Y")
            url = f"https://archive.twitter-trending.com/united-states/{formatted_date}"
            print(f"Scraping data for {formatted_date}...")
            
            scrape_trending_page(url, date, driver, timestamp)
            
    finally:
        print("All dates processed. Closing browser.")
        driver.quit()