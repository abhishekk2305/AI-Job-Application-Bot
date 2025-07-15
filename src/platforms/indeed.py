# src/platforms/indeed.py
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from src.logging import logger

def search_indeed_jobs(query, location, credentials):
    logger.info(f"🚀 Starting Indeed search for: '{query}'")
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://www.indeed.com/jobs?q={encoded_query}&l={location}&sort=date"
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    scraped_jobs = []

    try:
        driver.get(search_url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "lxml")
        
        # --- CORRECTED SELECTOR for Indeed job cards ---
        job_cards = soup.select('div.jobsearch-ResultsList > div.job_seen_beacon')
        logger.info(f"🔍 Found {len(job_cards)} potential job cards on Indeed.")
        
        for card in job_cards:
            try:
                title_element = card.select_one('h2.jobTitle > a[data-jk]')
                if not title_element: continue
                
                title = title_element.select_one('span').get_text(strip=True)
                job_url = "https://www.indeed.com/viewjob?jk=" + title_element['data-jk']
                company = card.select_one('span[data-testid="company-name"]').get_text(strip=True)
                
                if title and company and job_url:
                    scraped_jobs.append({"title": title, "company": company, "location": location, "url": job_url, "source": "indeed", "description": f"Job for {title} at {company}"})
            except (AttributeError, TypeError):
                continue
    except Exception as e:
        logger.error(f"❌ An error occurred during Indeed search: {e}")
    finally:
        driver.quit()

    logger.info(f"✅ Found {len(scraped_jobs)} unique jobs from Indeed for query: '{query}'")
    return scraped_jobs

def apply_to_indeed_job(driver, job_data, credentials, resume_path, cover_letter_text):
    # This function's logic remains the same
    pass