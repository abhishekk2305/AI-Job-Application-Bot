import os
import csv
from pathlib import Path
from src.logging import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.platforms.linkedin import apply_to_linkedin_job
from src.platforms.indeed import apply_to_indeed_job
from src.platforms.wellfound import apply_to_wellfound_job
from src.platforms.remoteok import apply_to_remoteok_job

MANUAL_LOG_FILE = Path("manual_applications.csv")

def log_manual_application(job_data):
    with open(MANUAL_LOG_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([job_data.get("company",""), job_data.get("title",""), job_data.get("url","")])

def apply_to_job(job_data, credentials, resume_text, cover_letter_text):
    platform = job_data.get("source", "").lower()
    logger.info(f"💼 Processing application on '{platform}' for: {job_data.get('title')}")
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    temp_dir = os.getcwd()
    resume_path = os.path.join(temp_dir, "temp_resume.txt")
    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(resume_text)

    try:
        if platform == "linkedin":
            apply_to_linkedin_job(driver, job_data, credentials, resume_path, cover_letter_text)
        elif platform == "indeed":
            apply_to_indeed_job(driver, job_data, credentials, resume_path, cover_letter_text)
        elif platform == "wellfound":
            apply_to_wellfound_job(driver, job_data, credentials, resume_path, cover_letter_text)
        elif platform == "remoteok":
            apply_to_remoteok_job(driver, job_data, credentials, resume_path, cover_letter_text)
        else:
            raise NotImplementedError(f"Application logic for {platform} not implemented.")
        logger.info(f"✅ Successfully submitted application for: {job_data.get('title')}")
        return "SUCCESS"
    except Exception as e:
        if any(phrase in str(e).lower() for phrase in ["external site", "not an on-site", "not an easy apply"]):
            logger.warning(f"⚠️ External application or manual step required: {job_data.get('title')}")
            log_manual_application(job_data)
            return "MANUAL_REQUIRED"
        else:
            logger.error(f"❌ Application failed: {e}")
            return f"FAILED: {e}"
    finally:
        driver.quit()
        if os.path.exists(resume_path):
            os.remove(resume_path)