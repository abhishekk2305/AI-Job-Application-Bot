import csv
from pathlib import Path
import datetime
from .logging import logger

LOG_FILE = Path("application_log.csv")

def save_application_details(job_data, status):
    try:
        file_exists = LOG_FILE.exists()
        with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Timestamp", "Company", "Title", "Source", "Status"])
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([
                timestamp,
                job_data.get('company', 'N/A'),
                job_data.get('title', 'N/A'),
                job_data.get('source', 'N/A'),
                status
            ])
    except Exception as e:
        logger.error(f"❌ Failed to write log: {e}")