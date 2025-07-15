# main.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from src.logging import logger
from src.job_application import apply_to_job
from src.job_application_saver import save_application_details
from src.platforms.linkedin import search_linkedin_jobs
from src.platforms.indeed import search_indeed_jobs
from src.platforms.wellfound import search_wellfound_jobs
from src.platforms.remoteok import search_remoteok_jobs
from src.resume_builder import generate_resume
from src.cover_letter_builder import generate_cover_letter

PLATFORM_SEARCH_FUNCTIONS = {
    "linkedin": search_linkedin_jobs,
    "indeed": search_indeed_jobs,
    "wellfound": search_wellfound_jobs,
    "remoteok": search_remoteok_jobs,
}

def load_config():
    with open("config.yaml", 'r') as f:
        return yaml.safe_load(f)

def load_credentials():
    load_dotenv()
    return {
        key: os.getenv(key) for key in [
            "OPENAI_API_KEY", "LINKEDIN_USER", "LINKEDIN_PASSWORD",
            "WELLFOUND_USER", "WELLFOUND_PASSWORD",
            "APPLICANT_FULL_NAME", "APPLICANT_PHONE", "APPLICANT_ADDRESS",
            "APPLICANT_LINKEDIN_PROFILE", "APPLICANT_WEBSITE"
        ]
    }

def main():
    config = load_config()
    credentials = load_credentials()
    logger.info("✅ Loaded configuration and credentials.")

    apply_limit = config.get('apply_limit', 5) 
    applied_count = 0

    job_titles = config.get('job_titles', [])
    sector_keywords = config.get('sector_keywords', [])
    location = config.get('location', 'Remote')
    region = config.get('search_region', '')
    platforms = config.get('platforms_to_scrape', [])
    
    resume_template_path = Path("resume_template.txt")
    if not resume_template_path.exists():
        logger.error("❌ resume_template.txt not found! It is required for AI generation.")
        return
    resume_template = resume_template_path.read_text()

    for platform in platforms:
        if applied_count >= apply_limit: break
        if platform not in PLATFORM_SEARCH_FUNCTIONS: continue
        
        search_func = PLATFORM_SEARCH_FUNCTIONS[platform]
        
        search_queries = {f"{title} {keyword}" for title in job_titles for keyword in sector_keywords}
        
        for query in search_queries:
            if applied_count >= apply_limit:
                logger.info(f"🏁 Reached application limit of {apply_limit}. Stopping all searches.")
                break

            full_query = f"{query} in {region}"
            found_jobs = search_func(full_query, location, credentials)

            if not found_jobs:
                continue

            logger.info(f"✅ Found {len(found_jobs)} jobs from {platform}. Starting application process for this batch...")
            
            for job in found_jobs:
                if applied_count >= apply_limit: break

                try:
                    logger.info(f"\n--- Applying to: {job.get('title')} at {job.get('company')} ---")
                    job_description = job.get("description", "No description available.")
                    
                    logger.info(f"🤖 Generating tailored resume and cover letter...")
                    resume_text = generate_resume(credentials["OPENAI_API_KEY"], job_description, resume_template)
                    cover_letter_text = generate_cover_letter(credentials["OPENAI_API_KEY"], job_description, "Please write a compelling cover letter.")
                    
                    status = apply_to_job(job, credentials, resume_text, cover_letter_text)
                    save_application_details(job, status)

                    if "SUCCESS" in status:
                        applied_count += 1
                except Exception as e:
                    logger.error(f"❌ A critical error occurred during the application process for {job.get('title')}: {e}")
                    save_application_details(job, f"CRITICAL_FAILURE: {e}")

    logger.info(f"\n🎯 Job application session completed. Processed {applied_count} applications.")

if __name__ == "__main__":
    main()