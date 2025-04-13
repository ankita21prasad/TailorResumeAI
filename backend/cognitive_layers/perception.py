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
    Extract the following information from the job description:
    - Skills (as a list)
    - Responsibilities (as a list)
    - Tone (e.g., Formal, Informal)
    - Company Values (as a list)

    Job Description:
    {job_text}

    Return a JSON object.
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