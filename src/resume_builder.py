# src/resume_builder.py
from openai import OpenAI
from src.logging import logger

def generate_resume(api_key, job_description, base_resume):
    logger.info("Generating resume using OpenAI GPT...")
    try:
        # Modern way to initialize the client (v1.0.0+)
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Based on the following base resume and the job description for the role below, create a tailored, professional, one-page resume.
        Focus on highlighting the most relevant skills and experiences. Ensure the output is clean and well-formatted.

        Base Resume:
        ---
        {base_resume}
        ---

        Job Description:
        ---
        {job_description}
        ---

        Tailored Resume:
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )
        
        tailored_resume = response.choices[0].message.content.strip()
        logger.info("✅ Resume generated successfully.")
        return tailored_resume
    except Exception as e:
        logger.error(f"❌ OpenAI resume generation failed: {e}")
        # Re-raise the exception to be caught by the main loop
        raise