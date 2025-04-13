# backend/cognitive_layers/action.py
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_cover_letter(resume_data, jd_data, matched_skills, user_preferences, tone='Formal'):
    """
    Generate a cover letter using Gemini.
    """
    role_title = jd_data.get('Title', 'the position') if jd_data else 'the position'
    company = jd_data.get('Company', 'the company') if jd_data else 'the company'

    prompt = f"""
    Generate a cover letter for {role_title} at {company}.
    Use a {tone} tone.
    Here are my skills: {matched_skills}.
    Here is my resume: {resume_data}.
    Here are my preferences: {user_preferences}.
    """
    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
    return response.text

def get_llm_response(prompt):
    """
    Get a response from the Gemini model.
    """
    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
    return response.text