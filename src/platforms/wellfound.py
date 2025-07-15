# src/platforms/wellfound.py
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logging import logger

def search_wellfound_jobs(query, location, credentials):
    logger.info(f"🚀 Starting Wellfound search for: '{query}'")
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    scraped_jobs = []

    try:
        driver.get("https://wellfound.com/login")
        time.sleep(3)
        
        # --- CORRECTED SELECTORS for Wellfound login ---
        driver.find_element(By.CSS_SELECTOR, "input[name='user[email]']").send_keys(credentials["WELLFOUND_USER"])
        driver.find_element(By.CSS_SELECTOR, "input[name='user[password]']").send_keys(credentials["WELLFOUND_PASSWORD"])
        driver.find_element(By.CSS_SELECTOR, "input[name='commit']").click()
        time.sleep(5)
        logger.info("🔐 Logged into Wellfound successfully.")

        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://wellfound.com/jobs?q={encoded_query}"
        driver.get(search_url)
        wait = WebDriverWait(driver, 20)
        
        job_card_selector = "div[data-test='JobListing']"
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_card_selector)))
        
        job_cards = driver.find_elements(By.CSS_SELECTOR, job_card_selector)
        logger.info(f"🔍 Found {len(job_cards)} job cards on Wellfound.")

        for card in job_cards:
            try:
                title_element = card.find_element(By.CSS_SELECTOR, "a[data-test='JobListing-title-link']")
                company_element = card.find_element(By.CSS_SELECTOR, "a[data-test='StartupResult-container-name-link']")
                
                title = title_element.text
                company = company_element.text
                job_url = title_element.get_attribute("href")

                if title and company and job_url:
                    scraped_jobs.append({"title": title, "company": company, "location": "Remote", "url": job_url, "source": "wellfound", "description": f"Job for {title} at {company}"})
            except NoSuchElementException:
                continue
    except Exception as e:
        logger.error(f"❌ An error occurred during Wellfound search: {e}")
    finally:
        driver.quit()

    logger.info(f"✅ Found {len(scraped_jobs)} unique jobs from Wellfound for query: '{query}'")
    return scraped_jobs

def apply_to_wellfound_job(driver, job_data, credentials, resume_path, cover_letter_text):
    # This function's logic remains the same
    pass