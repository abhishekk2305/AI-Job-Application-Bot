# src/cover_letter_builder.py
from openai import OpenAI
from src.logging import logger

def generate_cover_letter(api_key, job_description, prompt_text):
    logger.info("Generating cover letter using OpenAI GPT...")
    try:
        # Modern way to initialize the client (v1.0.0+)
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Based on the following job description, write a compelling, professional, and concise cover letter.
        Use the following guiding prompt: "{prompt_text}"
        
        Job Description:
        ---
        {job_description}
        ---
        
        Cover Letter:
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8
        )
        
        cover_letter = response.choices[0].message.content.strip()
        logger.info("✅ Cover letter generated successfully.")
        return cover_letter
    except Exception as e:
        logger.error(f"❌ OpenAI cover letter generation failed: {e}")
        # Re-raise the exception to be caught by the main loop
        raise
