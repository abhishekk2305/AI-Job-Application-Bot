# src/platforms/linkedin.py
import time
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.logging import logger

def search_linkedin_jobs(query, location, credentials):
    logger.info(f"🚀 Starting LinkedIn search for: '{query}'")
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    scraped_jobs = []

    try:
        driver.get("https://www.linkedin.com/login")
        time.sleep(3)
        driver.find_element(By.ID, "username").send_keys(credentials["LINKEDIN_USER"])
        driver.find_element(By.ID, "password").send_keys(credentials["LINKEDIN_PASSWORD"])
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        logger.info("🔐 Logged into LinkedIn successfully for search.")

        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_query}&location={location}&f_WT=2&f_LF=f_AL&sortBy=R"
        driver.get(search_url)

        if "/checkpoint/" in driver.current_url:
            raise Exception("LinkedIn is asking for a security check (CAPTCHA).")

        wait = WebDriverWait(driver, 20)
        job_card_selector = "div.job-search-card"
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, job_card_selector)))
        
        time.sleep(2)
        job_cards = driver.find_elements(By.CSS_SELECTOR, job_card_selector)
        
        for card in job_cards:
            try:
                title_element = card.find_element(By.CSS_SELECTOR, "h3.base-search-card__title")
                company_element = card.find_element(By.CSS_SELECTOR, "h4.base-search-card__subtitle")
                url_element = card.find_element(By.CSS_SELECTOR, "a.base-card__full-link")
                title = title_element.text
                company = company_element.text
                job_url = url_element.get_attribute("href").split('?')[0]
                
                if title and company and job_url:
                    scraped_jobs.append({"title": title, "company": company, "location": location, "url": job_url, "source": "linkedin", "description": f"Job for {title} at {company}"})
            except NoSuchElementException:
                continue
    except Exception as e:
        logger.error(f"❌ An error occurred during LinkedIn search: {e}")
    finally:
        driver.quit()
    logger.info(f"✅ Found {len(scraped_jobs)} unique jobs from LinkedIn for query: '{query}'")
    return scraped_jobs

def apply_to_linkedin_job(driver, job_data, credentials, resume_path, cover_letter_text):
    driver.get(job_data['url'])
    wait = WebDriverWait(driver, 15)
    
    try:
        easy_apply_button_xpath = "//button[contains(@class, 'jobs-apply-button')]"
        easy_apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, easy_apply_button_xpath)))
        easy_apply_button.click()
        time.sleep(2)
    except TimeoutException:
        raise Exception("Not an 'Easy Apply' job (button did not load).")

    while True:
        try:
            submit_button = driver.find_element(By.XPATH, "//button[@aria-label='Submit application']")
            # submit_button.click() # UNCOMMENT TO SUBMIT
            logger.warning("LinkedIn Apply: Submit button found but not clicked.")
            time.sleep(2)
            return
        except NoSuchElementException:
            try:
                next_button = driver.find_element(By.XPATH, "//button[@aria-label='Continue to next step']")
                next_button.click()
                time.sleep(2)
            except NoSuchElementException:
                raise Exception("Could not find Next or Submit button.")