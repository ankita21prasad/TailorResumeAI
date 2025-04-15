# backend/main.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from cognitive_layers import perception, memory, decision_making, action
from dotenv import load_dotenv
from cognitive_layers.decision_making import Skills

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Memory
user_memory = memory.Memory()

@app.route('/get-user-preferences', methods=['POST'])
def get_user_preferences():
    """
    Endpoint to get user preferences.
    """
    preferences = request.json
    user_memory.store('user_preferences', preferences)
    return jsonify({'message': 'User preferences stored successfully!'})

@app.route('/process-job-application', methods=['POST'])
def process_job_application():
    """
    Main endpoint to process job application.
    """
    job_text = request.form['job_text']  # <-- change this
    resume_file = request.files['resume']

    # 1. Perception Layer
    jd_data = perception.parse_job_description(job_text)
    print("JD data", jd_data)
    resume_text = perception.parse_resume(resume_file)
    print("Resume text", resume_text)

    # 2. Memory Layer
    user_preferences = user_memory.retrieve('user_preferences')

    # 3. Decision-Making Layer
    skills_data: Skills = decision_making.match_skills(resume_text, jd_data)
    print(skills_data)
    resume_improvements = decision_making.suggest_resume_improvements(resume_text, jd_data)
    print(resume_improvements)

    # 4. Action Layer
    cover_letter = action.generate_cover_letter(resume_text, jd_data, skills_data.matched_skills, user_preferences)
    print(cover_letter)


    return jsonify({
        'matched_skills': skills_data.matched_skills,
        'missing_skills': skills_data.missing_skills,
        'cover_letter': cover_letter,
        'resume_improvements': resume_improvements
    })

if __name__ == '__main__':
    app.run(debug=True)