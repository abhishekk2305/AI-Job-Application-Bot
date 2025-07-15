# 🤖 AI-Powered Job Application Bot

An intelligent Python bot that automates the tedious process of job searching and applying across multiple platforms like LinkedIn and Indeed.

---

## 🤔 The Problem
Job hunting is a full-time job. Manually searching for roles, tailoring resumes, and writing unique cover letters for hundreds of applications is a repetitive and time-consuming process. I built this bot to automate the 99% of that work.

## ✨ Key Features
- **Multi-Platform Scraping**: Searches for jobs on LinkedIn, Indeed, and more.
- **AI-Powered Customization**: Uses the OpenAI API (GPT) to write a unique resume and cover letter tailored to **each specific job description**.
- **Intelligent Application Handling**:
    - Attempts to automatically apply to compatible "Easy Apply" jobs.
    - Identifies jobs on external sites and saves them to a `manual_applications.csv` for you to review.
- **Comprehensive Logging**: Tracks every success, failure, and manual application in organized `.csv` files.
- **Configurable**: Easily change job titles, keywords, and platforms to search via a `config.yaml` file.

## 🛠️ Tech Stack
- **Language**: Python
- **Automation**: Selenium
- **Web Scraping**: BeautifulSoup
- **AI**: OpenAI API
- **Configuration**: YAML, Dotenv

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- Google Chrome

### 2. Installation
Clone the repository and install the required packages:
```bash
git clone [https://github.com/](https://github.com/)[YOUR_USERNAME]/AI-Job-Application-Bot.git
cd AI-Job-Application-Bot
pip install -r requirements.txt
