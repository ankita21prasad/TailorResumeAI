import os
import re
import json
from google import genai
from dotenv import load_dotenv
# from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
load_dotenv()

# Access your API key and initialize Gemini client correctly
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def parse_job_description(job_text):
    print(job_text)
    prompt = prompt = f"""
You are a job description analysis assistant.

Given the following job description, extract the key structured elements:
- Job Title
- Required Skills
- Preferred Skills (if any)
- Key Responsibilities
- Tone of the description (formal, friendly, technical, etc.)
- Any mention of company culture or values

Return the output in the following JSON format:

{{
  "job_title": "",
  "required_skills": [],
  "preferred_skills": [],
  "responsibilities": [],
  "tone": "",
  "company_values": []
}}

Job Description:
{job_text}

Ensure you always return the json response without any backticks with given keys even if empty.
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

def parse_resume(resume_file):
    try:
        # Handle PDF files
        if resume_file.filename.endswith('.pdf'):
            # Reset file pointer and parse using pdfminer.six
            resume_file.stream.seek(0)
            laparams = LAParams()  # You can adjust the parameters if needed
            text = extract_text(resume_file.stream, laparams=laparams)
        
        # Handle text files
        elif resume_file.filename.endswith('.txt'):
            # Read text file content
            resume_file.stream.seek(0)  # Make sure to reset the file pointer
            text = resume_file.read().decode('utf-8')
        # Handle JSON files
        elif resume_file.filename.endswith('.json'):
            # Read JSON file content
            resume_file.stream.seek(0)  # Reset file pointer
            json_data = json.load(resume_file.stream)  # Parse JSON content
            text = json.dumps(json_data, indent=4) 
        
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT files are allowed.")

        return text
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return ""

def match_skills(resume_data, jd_data):
    SKILL_MATCH_PROMPT = f"""
You are a job matching assistant.

Compare the candidate’s resume data with the job description data.

- Identify which required skills are present.
- Identify missing skills.
- Highlight work experience that best matches the role.
- Optionally recommend areas to strengthen.

Resume Skills:
{resume_data}

Job Required Skills:
{jd_data}

Return structured JSON:
{{
  "matched_skills": [],
  "missing_skills": [],
  "perfect_fit_experience": [],
  "recommendations": []
}}

Ensure you always return the json response without any backticks with given keys even if empty.
"""

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=SKILL_MATCH_PROMPT
                )
    
    text = re.sub(r"^```(?:json)?\n|```$", "", response.text.strip(), flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {text}")
        return {}

def generate_cover_letter(resume_data, jd_data, matched_skills, tone='Formal'):
    print(resume_data, jd_data, matched_skills)
    role_title = jd_data.get('Title', 'the position') if jd_data else 'the position'
    company = jd_data.get('Company', 'the company') if jd_data else 'the company'

    COVER_LETTER_PROMPT = f"""
Write a tailored cover letter for the following job, using the tone: {tone}.

Use the resume data to highlight relevant skills and experiences.

Make it feel human and authentic — no generic filler.

Return only the letter content (no headers or explanations).

Job Title: {role_title}
Company: {company}

Resume Summary:
{resume_data}

Matched Skills: {matched_skills}
"""

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=COVER_LETTER_PROMPT
                )
    return response.text

def suggest_resume_improvements(resume_data, jd_data):
    RESUME_IMPROVE_PROMPT = prompt = f"""
You are a resume improvement assistant.

Given the job description and current resume data, suggest edits to better align the resume with the role.

Only suggest factual edits based on existing experiences.

Focus on:
- Wording changes
- Highlighting relevant achievements
- Removing irrelevant content

Return in this format:
{{
  "section_suggestions": {{
    "Experience": ["Suggest rephrasing X to emphasize Y", "..."],
    "Skills": ["Add Z skill if applicable", "..."]
  }},
  "general_tips": ["Keep bullet points action-oriented", "..."]
}}

Job Description:
{jd_data}

Resume Data:
{resume_data}

Ensure you always return the json response without any backticks with given keys even if empty.
"""


    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=RESUME_IMPROVE_PROMPT
                )
    text = re.sub(r"^```(?:json)?\n|```$", "", response.text.strip(), flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {text}")
        return {}