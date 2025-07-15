# src/platforms/remoteok.py
import requests
from bs4 import BeautifulSoup
from src.logging import logger
import urllib.parse

def search_remoteok_jobs(query, location, credentials):
    logger.info(f"🚀 Starting RemoteOK search for: '{query}'")
    encoded_query = urllib.parse.quote_plus(query)
    search_url = f"https://remoteok.com/remote-{encoded_query}-jobs"
    scraped_jobs = []
    
    try:
        response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() # Will raise an error for bad status codes
        soup = BeautifulSoup(response.text, 'lxml')
        
        job_cards = soup.find_all("tr", class_="job")
        logger.info(f"🔍 Found {len(job_cards)} job cards on RemoteOK.")
        
        for card in job_cards:
            try:
                title_element = card.find("h2", itemprop="title")
                company_element = card.find("h3", itemprop="name")
                url_element = card.find("a", class_="preventLink", itemprop="url")

                if not (title_element and company_element and url_element):
                    continue

                title = title_element.text.strip()
                company = company_element.text.strip()
                job_url = "https://remoteok.com" + url_element["href"]
                
                if title and company and job_url:
                    scraped_jobs.append({"title": title, "company": company, "location": "Remote", "url": job_url, "source": "remoteok", "description": f"Job for {title} at {company}"})
            except (AttributeError, TypeError):
                continue
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Could not fetch RemoteOK page: {e}")
    except Exception as e:
        logger.error(f"❌ An error occurred during RemoteOK search: {e}")

    logger.info(f"✅ Found {len(scraped_jobs)} unique jobs from RemoteOK for query: '{query}'")
    return scraped_jobs

def apply_to_remoteok_job(driver, job_data, credentials, resume_path, cover_letter_text):
    # RemoteOK almost always links to an external site.
    # This function identifies that and triggers the manual save.
    raise Exception("Not an on-site application (external site).")