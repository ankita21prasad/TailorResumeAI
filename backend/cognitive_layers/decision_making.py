# backend/cognitive_layers/decision_making.py
import re, json, os
from google import genai
from pydantic import BaseModel
from typing import List
from cognitive_layers.action import get_llm_response, parse_gemini_response

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

class ResumeImprovements(BaseModel):
    resume_improvements: List[str]

class Skills(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    highlight_areas: str

def match_skills(resume_data, jd_data):
    """
    Compare resume skills with job description skills.
    """

    prompt = f"""
You are an expert AI-powered career assistant.

Your task is to analyze a candidate's resume and compare it against the required skills from a job description. Use structured, step-by-step reasoning to ensure accuracy.

Instructions:
1. Read the job description carefully and extract the list of required skills.
2. Read the resume thoroughly and identify all skills mentioned, including synonyms or equivalent terms.
3. Compare both lists to determine:
   - Which skills are clearly present in the resume (matched_skills).
   - Which skills are missing or weakly mentioned (missing_skills).
4. Write a recommendation (highlight_areas) advising how the candidate could modify their resume to better reflect the missing skills. Suggest specific sections (e.g., Technical Skills, Projects, Experience) to update.
5. If unsure about any skill match, flag it clearly in the missing_skills list or explain it in the recommendation.
6. Sanity-check your output for alignment with the job description and resume content before finalizing.

**Return the output ONLY in following JSON format:**
{{
  "matched_skills": [],
  "missing_skills": [],
  "highlight_areas": ""
}}
Do not include any extra commentary or markdown (e.g., no ```json or explanation).

Job Description: {jd_data}

Resume: {resume_data}
"""

    response_text = get_llm_response(prompt=prompt)
    skills = parse_gemini_response(response_text=response_text, output_model=Skills)

    return skills

def suggest_resume_improvements(resume_data, jd_data):
    """
    Suggest resume improvements based on job description.
    """
    prompt = f"""
You are an expert AI career assistant.

Your task is to analyze a candidate’s resume and compare it with a job description to suggest minor, factual edits that improve alignment with the role.

Instructions:
1. Carefully read the resume and the job description.
2. Think step-by-step to identify small but impactful changes (e.g., rephrasing, keyword optimization, adding minor achievements, etc.).
3. Ensure all suggestions are factual and based on existing content in the resume.
4. Focus on minor tweaks only—do not fabricate experiences.
5. Sanity-check suggestions to avoid redundancy or exaggeration.
6. If you're unsure about a change, skip it or provide a fallback phrasing.
7. Ensure no points in resume_improvements are repeated.

**Return the output ONLY in following JSON format:**
{{
  "resume_improvements": [
    "First improvement",
    "Second improvement",
    "Third improvement"
  ]
}}
Do not include any extra commentary or markdown (e.g., no ```json or explanation).

Resume: {resume_data}

Job Description: {jd_data}
"""
    
    response_text = get_llm_response(prompt=prompt)
    resume_improvements = parse_gemini_response(response_text=response_text, output_model=ResumeImprovements)

    return resume_improvements.resume_improvements