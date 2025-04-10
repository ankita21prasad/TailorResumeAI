document.addEventListener('DOMContentLoaded', function() {
    const jobDescriptionInput = document.getElementById('jobDescription');
    const resumeUploadInput = document.getElementById('resumeUpload');
    const analyzeButton = document.getElementById('analyzeButton');
    const skillsMatchedDiv = document.getElementById('skillsMatched');
    const missingSkillsDiv = document.getElementById('missingSkills');
    const coverLetterTextarea = document.getElementById('coverLetterText');
    const resumeImprovementsDiv = document.getElementById('resumeImprovements');
    const copyButton = document.getElementById('copyButton');
    const downloadButton = document.getElementById('downloadButton');
    const emailButton = document.getElementById('emailButton');

    analyzeButton.addEventListener('click', async () => {
        const jobText = jobDescriptionInput.value;
        const resumeFile = resumeUploadInput.files[0];

        // --- 1. Parse Job Description ---
        const jdData = await parseJobDescription(jobText);

        // --- 2. Upload and Parse Resume ---
        const resumeText = await uploadResume(resumeFile);

        // --- 3. Match Skills ---
        const skillsData = await matchSkills(resumeText, jdData);

        // --- 4. Generate Cover Letter ---
        const coverLetter = await generateCoverLetter(resumeText, jdData, skillsData.matched_skills);

        // --- 5. Suggest Resume Improvements ---
        const resumeEdits = await suggestResumeImprovements(resumeText, jdData);

        // --- Update UI ---
        skillsMatchedDiv.textContent = 'Matched Skills: ' + skillsData.matched_skills.join(', ');
        missingSkillsDiv.textContent = 'Missing Skills: ' + skillsData.missing_skills.join(', ');
        coverLetterTextarea.value = coverLetter;
        resumeImprovementsDiv.textContent = 'Resume Improvements: ' + resumeEdits;
    });

    copyButton.addEventListener('click', () => {
        coverLetterTextarea.select();
        document.execCommand('copy');
    });

    downloadButton.addEventListener('click', () => {
        const text = coverLetterTextarea.value;
        const filename = "cover_letter.txt";

        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);

        element.style.display = 'none';
        document.body.appendChild(element);

        element.click();

        document.body.removeChild(element);
    });

    emailButton.addEventListener('click', () => {
        const text = coverLetterTextarea.value;
        const subject = "Cover Letter";
        const body = encodeURIComponent(text);
        window.open(`mailto:?subject=${subject}&body=${body}`);
    });

    // --- Helper Functions ---
    async function parseJobDescription(jobText) {
        const response = await fetch('http://127.0.0.1:5000/parse-job-description', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ job_text: jobText })
        });
        return await response.json();
    }

    async function uploadResume(resumeFile) {
        const formData = new FormData();
        formData.append('resume', resumeFile);

        const response = await fetch('http://127.0.0.1:5000/upload-resume', {
            method: 'POST',
            body: formData
        });
        const data =  await response.json();
        return data.resume_text;
    }

    async function matchSkills(resumeText, jdData) {
        const response = await fetch('http://127.0.0.1:5000/match-skills', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ resume_data: resumeText, jd_data: jdData })
        });
        return await response.json();
    }

    async function generateCoverLetter(resumeText, jdData, matchedSkills) {
        const response = await fetch('http://127.0.0.1:5000/generate-cover-letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ resume_data: resumeText, jd_data: jdData, matched_skills: matchedSkills })
        });
        const data = await response.json();
        return data.cover_letter;
    }

    async function suggestResumeImprovements(resumeText, jdData) {
        const response = await fetch('http://127.0.0.1:5000/suggest-resume-edits', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ resume_data: resumeText, jd_data: jdData })
        });
        const data = await response.json();
        return data.suggestions;
    }
});