import os
import io
import re
import json
import pdfminer.high_level
from pdfminer.layout import LAParams
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def parse_job_description(job_text):
    prompt = """
You are a job description analysis assistant.

Given the following job description, extract the key structured elements:
- Job Title
- Required Skills
- Preferred Skills (if any)
- Key Responsibilities
- Tone of the description (formal, friendly, technical, etc.)
- Any mention of company culture or values

Return the output in the following JSON format:

{
  "job_title": "",
  "required_skills": [],
  "preferred_skills": [],
  "responsibilities": [],
  "tone": "",
  "company_values": []
}

Job Description:
{job_text}
""".format(job_text=job_text)
    
    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {response.text}")
        return {}

def parse_resume(resume_file):
    try:
        if resume_file.filename.endswith('.pdf'):
            # Parse PDF
            laparams = LAParams()
            text = pdfminer.high_level.extract_text(resume_file, laparams=laparams)
        else:
            # Assume it's a text file
            text = resume_file.read().decode('utf-8')
        return text
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""

def match_skills(resume_data, jd_data):
    SKILL_MATCH_PROMPT = """
You are a job matching assistant.

Compare the candidate’s resume data with the job description data.

- Identify which required skills are present.
- Identify missing skills.
- Highlight work experience that best matches the role.
- Optionally recommend areas to strengthen.

Resume Skills:
{resume_skills}

Job Required Skills:
{jd_skills}

Return structured JSON:
{
  "matched_skills": [],
  "missing_skills": [],
  "perfect_fit_experience": [],
  "recommendations": []
}
""".format(resume_skills=resume_data,
           jd_skills=jd_data)

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=SKILL_MATCH_PROMPT
                )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {response.text}")
        return {}

def generate_cover_letter(resume_data, jd_data, matched_skills, tone='Formal'):
    role_title = jd_data.get('Title', 'the position') if jd_data else 'the position'
    company = jd_data.get('Company', 'the company') if jd_data else 'the company'

    COVER_LETTER_PROMPT = """
Write a tailored cover letter for the following job, using the tone: {tone_style}.

Use the resume data to highlight relevant skills and experiences.

Make it feel human and authentic — no generic filler.

Return only the letter content (no headers or explanations).

Job Title: {job_title}
Company: {company_name}

Resume Summary:
{resume_summary}

Matched Skills: {matched_skills}

Additional Notes (if any): {notes}
""".format(job_title = role_title,
           company_name = company,
           resume_summary = resume_data,
           matched_skills = matched_skills
           )

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=COVER_LETTER_PROMPT
                )
    return response.text

def suggest_resume_improvements(resume_data, jd_data):
    RESUME_IMPROVE_PROMPT = """
You are a resume improvement assistant.

Given the job description and current resume data, suggest edits to better align the resume with the role.

Only suggest factual edits based on existing experiences.

Focus on:
- Wording changes
- Highlighting relevant achievements
- Removing irrelevant content

Return in this format:
{
  "section_suggestions": {
    "Experience": ["Suggest rephrasing X to emphasize Y", ...],
    "Skills": ["Add Z skill if applicable", ...]
  },
  "general_tips": ["Keep bullet points action-oriented", ...]
}

Job Description:
{job_text}

Resume Data:
{resume_data}
""".format(job_text=jd_data,
           resume_data = resume_data)

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=RESUME_IMPROVE_PROMPT
                )
    return response.text