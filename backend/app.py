from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from utils import parse_job_description, parse_resume, match_skills, generate_cover_letter, suggest_resume_improvements
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

# Ensure the Gemini API key is set
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("No GOOGLE_API_KEY environment variable found. Please set it in .env.")

@app.route('/parse-job-description', methods=['POST'])
def parse_job_description_route():
    job_text = request.data.decode('utf-8')  # <-- changed from request.json
    print(job_text)
    data = parse_job_description(job_text)
    return jsonify(data)

@app.route('/upload-resume', methods=['POST'])
def upload_resume_route():
    resume_file = request.files['resume']
    print(resume_file)
    resume_text = parse_resume(resume_file)
    return jsonify({'resume_text': resume_text})

@app.route('/match-skills', methods=['POST'])
def match_skills_route():
    resume_data = request.json['resume_data']
    jd_data = request.json['jd_data']
    data = match_skills(resume_data, jd_data)
    return jsonify(data)

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_route():
    resume_data = request.json['resume_data']
    jd_data = request.json['jd_data']
    matched_skills = request.json['matched_skills']
    tone = request.json.get('tone', 'Formal')  # Default to 'Formal' if tone is not provided
    cover_letter = generate_cover_letter(resume_data, jd_data, matched_skills, tone)
    return jsonify({'cover_letter': cover_letter})

@app.route('/suggest-resume-edits', methods=['POST'])
def suggest_resume_edits_route():
    resume_data = request.json['resume_data']
    jd_data = request.json['jd_data']
    suggestions = suggest_resume_improvements(resume_data, jd_data)
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True)