from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selectolax_parser import parse_with_selectolax
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--start_date", type=str, default="01-01-2019", help="Start date in YYYY-MM-DD format")
parser.add_argument("--end_date", type=str, default="01-02-2019", help="End date in YYYY-MM-DD format")
args = parser.parse_args()

date_range = pd.date_range(start=args.start_date, end=args.end_date)
    
chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

def scrape_trending_page(url, date):
    try:
        driver.get(url)
        
        print("Waiting 10 seconds for JS to load...")
        time.sleep(10) 
        
        if "tt_list" in driver.page_source:
            print("Success: Tweet counts found!")
        else:
            print("Still not seeing tt_list in the source code.")    
        
        rendered_html = driver.page_source
        
        main_list, most_tweeted, longest_trending = parse_with_selectolax(rendered_html, date)
        timestamp = int(time.time())
        outpath = "out/"
        pd.DataFrame(main_list).to_csv(f"{outpath}trending_table_data_{timestamp}.csv", index=False, mode='a', header=not pd.io.common.file_exists(f"{outpath}trending_table_data_{timestamp}.csv"))
        pd.DataFrame(most_tweeted).to_csv(f"{outpath}most_tweeted_data_{timestamp}.csv", index=False, mode='a', header=not pd.io.common.file_exists(f"{outpath}most_tweeted_data_{timestamp}.csv"))
        pd.DataFrame(longest_trending).to_csv(f"{outpath}longest_trending_data_{timestamp}.csv", index=False, mode='a', header=not pd.io.common.file_exists(f"{outpath}longest_trending_data_{timestamp}.csv"))

    finally:
        driver.quit()
        
if __name__ == "__main__":
    for date in date_range:
        formatted_date = date.strftime("%d-%m-%Y")
        url = f"https://archive.twitter-trending.com/united-states/{formatted_date}"
        print(f"Scraping data for {formatted_date}...")
        scrape_trending_page(url, date)