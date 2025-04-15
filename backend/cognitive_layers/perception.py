# backend/cognitive_layers/perception.py
import os
import re
import json
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def parse_job_description(job_text):
    """
    Extract information from the job description using Gemini.
    """
    prompt = f"""
You are an information extraction assistant. Your task is to extract structured data from job descriptions using careful step-by-step reasoning.

Instructions:
1. First, read the job description carefully.
2. Identify relevant skills and responsibilities. Group them logically and clearly.
3. Determine the overall tone (e.g., Formal, Informal, Technical, Friendly).
4. Extract any statements about company values or culture.
5. Perform a quick self-check to verify your interpretation is consistent with the content.
6. If you are unsure about any section, leave it empty or include "unsure".

Do not include any extra commentary or markdown (e.g., no ```json or explanation).

Job Description: {job_text}

Before responding, think through each section carefully. Clearly separate your reasoning process from the final output using this structure:
Return the output in this JSON format: 
{{
  "skills": [],
  "responsibilities": [],
  "tone": "",
  "company_values": []
}}
Do not include any extra commentary or markdown (e.g., no ```json or explanation).
"""

    response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
    # Extract everything after "Final JSON output:" that looks like JSON
    print("===================================================")
    # print(response)
    try:
        return json.loads(response.text)
    except:
        match = re.search(r"Final JSON output:\s*(\{.*\})", response.text, re.DOTALL)
        if not match:
            match = re.search(r"```json\s*([\s\S]*?)\s*```", response.text)
        if match:
            json_text = match.group(1)
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            print(f"⚠️ Error decoding JSON from extracted text:\n{json_text}")
            return {response.text}

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