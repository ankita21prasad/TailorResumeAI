# backend/cognitive_layers/action.py
import os, json, re
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, Type, TypeVar
T = TypeVar('T', bound=BaseModel)

class CoverLetter(BaseModel):
    cover_letter: str

load_dotenv()

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
You are an expert AI assistant trained to generate personalized, professional cover letters.

Your task:
1. Carefully read the user's resume, matched skills, and preferences.
2. Analyze the job description to understand the tone, values, and required qualifications.
3. Think step-by-step before writing: match the resume strengths with the job’s requirements.
4. Use the user's tone and stylistic preferences throughout the letter.
5. Ensure that the final letter is concise, specific, and tailored to the company and role.
6. If information is missing (e.g., no company name), use a neutral fallback.
7. Do a quick self-check: does the letter sound personalized, and does it reflect both resume and job needs?

Return the output in this JSON format:
{{
  "cover_letter": "<insert personalized letter here>"
}}
Do not include any extra commentary or markdown (e.g., no ```json or explanation).

Job Title: {role_title}
Company: {company}
Tone: {tone}
Matched Skills: {matched_skills}
User Preferences: {user_preferences}

Resume: {resume_data}
"""
    
    response_text = get_llm_response(prompt=prompt)
    cover_letter = parse_gemini_response(response_text=response_text, output_model=CoverLetter)

    return cover_letter.cover_letter

def get_llm_response(prompt):
    """
    Get a response from the Gemini model.
    """
    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
    
    # If response is already a dict, return as-is
    if isinstance(response.text, dict):
        return json.dumps(response.text)
    if response.text.strip().startswith("```"):
        text = re.sub(r"^```(?:json)?\n|```$", "", response.text.strip(), flags=re.MULTILINE)
    try:
        return text.strip()
    except Exception as e:
        print(f"Error getting response: {e}")
        return {}

def parse_gemini_response(response_text: str, output_model: Type[T]) -> T:
    """
    Parses the Gemini API response into a specified Pydantic model.

    Args:
        response_text (str): Raw text output from Gemini.
        output_model (Type[T]): The Pydantic model class to parse the response into.

    Returns:
        An instance of output_model with the parsed data.

    Raises:
        ValueError: If the response is not valid JSON or doesn't match the model.
    """
    try:
        parsed_json = json.loads(response_text.strip())
        return output_model(**parsed_json)
    except json.JSONDecodeError:
        raise ValueError("Gemini output was not valid JSON.")
    except Exception as e:
        raise ValueError(f"Error parsing response: {e}")