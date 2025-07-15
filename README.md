# Fully Automated Job Application Bot

This bot automates finding and applying for jobs on multiple platforms, including LinkedIn and Indeed.

## Disclaimer

**This bot interacts with live websites. Websites change their design frequently, which will cause the bot to fail. This is not an error in the code, but the nature of web scraping. Expect to perform maintenance to keep the bot working.**

## Setup

1.  **Install Python**: Ensure you have Python 3.8 or newer.

2.  **Install Dependencies**: Open a terminal in the project folder and run:
    ```bash
    pip install -r requirements.txt
    ```
    If you haven't created the file yet, run these commands:
    ```bash
    python3 -m pip install python-dotenv PyYAML selenium openai beautifulsoup4 lxml
    ```

3.  **Create `.env` File**: Create a file named `.env` and fill it with your credentials and personal info. See `.env.example` for the required fields.

4.  **Configure Your Search**: Edit `config.yaml` to specify:
    - `job_titles`: Roles you are interested in.
    - `sector_keywords`: Industries to target.
    - `location` and `search_region`.
    - `platforms_to_scrape`: A list of websites to use (e.g., `linkedin`, `indeed`).

## How to Run

Once setup is complete, run the bot from your terminal:

```bash
python3 main.py