from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

    
chrome_options = Options()

# 1. REMOVE --headless (at least for testing)
# This opens a physical window so you can see if the data actually loads
# chrome_options.add_argument("--headless") 

# 2. Add a real window size
chrome_options.add_argument("--window-size=1920,1080")

# 3. Add a more convincing User-Agent
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)

url = "https://archive.twitter-trending.com/united-states/01-01-2019"

try:
    driver.get(url)
    
    # 4. Use a 'sleep' instead of 'wait.until' just to diagnose
    # This gives you time to manually look at the window and see if the numbers appear
    print("Waiting 10 seconds for JS to load...")
    time.sleep(10) 
    
    # Now check if tt_list is in the source
    if "tt_list" in driver.page_source:
        print("Success: Tweet counts found!")
    else:
        print("Still not seeing tt_list in the source code.")    # 3. Capture the fully rendered HTML
    
    rendered_html = driver.page_source
    soup = BeautifulSoup(rendered_html, 'html.parser')
    
    with open("trending.html", "w", encoding='utf-8') as f:
        f.write(soup.prettify())
    
finally:
    driver.quit()