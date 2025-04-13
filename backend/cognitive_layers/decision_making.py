# backend/cognitive_layers/decision_making.py
import re, json, os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def match_skills(resume_data, jd_data):
    """
    Compare resume skills with job description skills.
    """

    prompt = f"""
You are an expert career assistant.

Given the resume content and a list of required job skills, extract:
1. The list of matched skills that appear in the resume.
2. The list of missing or weakly mentioned skills.
3. A recommendation message on how to improve the resume to reflect the missing skills.

Return your answer in JSON format:
{{
  "matched_skills": [],
  "missing_skills": [],
  "highlight_areas": ""
}}

Job Description:
{jd_data}

Resume:
{resume_data}
    """

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
    text = re.sub(r"^```(?:json)?\n|```$", "", response.text.strip(), flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {text}")
        return {}

def suggest_resume_improvements(resume_data, jd_data):
    """
    Suggest resume improvements based on job description.
    """
    prompt = f"""
    Based on this resume: {resume_data} and this job description: {jd_data},
    suggest 3 minor tweaks to the resume to better align with the job description.
    """
    return prompt