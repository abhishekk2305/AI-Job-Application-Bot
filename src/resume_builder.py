# src/resume_builder.py
import os
from openai import OpenAI
from src.logging import logger

def generate_resume(api_key, job_description, base_resume_text):
    logger.info("Generating tailored resume using your experience...")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Based on my resume below, tailor it to perfectly match the following job description.
    Rewrite the professional summary and key skills to highlight what is most relevant.
    Do not invent new experience. Return only the tailored resume content in plain text.

    ---MY BASE RESUME---
    {base_resume_text}

    ---JOB DESCRIPTION---
    {job_description}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    result = response.choices[0].message.content.strip()
    logger.info("✅ Tailored resume generated successfully.")
    return result
