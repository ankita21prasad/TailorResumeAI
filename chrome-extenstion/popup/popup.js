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
    const loadingDiv = document.getElementById('loading');
    const loadingText = loadingDiv.querySelector('.loading-text');

    const loadingMessages = [
        "Analyzing job description...",
        "Scanning resume...",
        "Matching skills with role requirements...",
        "Identifying key achievements...",
        "Reviewing experience highlights...",
        "Crafting personalized suggestions...",
        "Checking alignment with job criteria...",
        "Finalizing your tailored application...",
        "Almost done...",
        "Crafting suggestions...",
        "Almost done..."
    ];

    let loadingMessageIndex = 0;
    let loadingInterval = null;

    analyzeButton.addEventListener('click', async () => {
        const jobText = jobDescriptionInput.value;
        const resumeFile = resumeUploadInput.files[0];
        // const preferences = JSON.parse(preferencesInput.value); // Parse user preferences
        const preferences = {
            "preferred_resume_tone": preferred_resume_tone.value,
            "what_to_highlight_most": what_to_highlight_most.value,
            "current_experience_level": current_experience_level.value,
            "personal_style_preferences": personal_style_preferences.value
        };

        // --- Store User Preferences ---
        await storeUserPreferences(preferences);
        // --- Show Loading Buffer ---
        showLoading();
        try {
            // --- Process Job Application ---
            const results = await processJobApplication(jobText, resumeFile);

            // --- Update UI ---
            skillsMatchedDiv.textContent = 'Matched Skills: ' + results.matched_skills.join(', ');
            missingSkillsDiv.textContent = 'Missing Skills: ' + results.missing_skills.join(', ');
            coverLetterTextarea.value = results.cover_letter;
            // Format resume improvements
            // const improvements = results.resume_improvements; 
            // const listItems = improvements.map(item => `<li>${item}</li>`).join('');
            console.log(results.resume_improvements)
            renderResumeImprovements(results.resume_improvements, resumeImprovementsDiv); //`<ul>${listItems}</ul>`;
        } finally {
            // --- Hide Loading Buffer ---
            hideLoading();
        }
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
    async function storeUserPreferences(preferences) {
        const response = await fetch('http://127.0.0.1:5000/get-user-preferences', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(preferences)
        });
        return await response.json();
    }

    async function processJobApplication(jobText, resumeFile) {
        const formData = new FormData();
        formData.append('resume', resumeFile);
        formData.append('job_text', jobText);
        console.log(formData)

        const response = await fetch('http://127.0.0.1:5000/process-job-application', {
            method: 'POST',
            body: formData
        });
        return await response.json();
    }
    function renderResumeImprovements(rawText, container) {
        container.innerHTML = ''; // Clear any existing content
    
        // Create section title
        const sectionTitle = document.createElement('h2');
        sectionTitle.textContent = 'Resume improvements';
        sectionTitle.style.textAlign = 'center'; 
        container.appendChild(sectionTitle);
    
        // Optional intro paragraph
        const introParagraph = document.createElement('p');
        introParagraph.textContent = "(These suggestions can help improve your resume's impact)";
        introParagraph.style.textAlign = 'center'; 
        container.appendChild(introParagraph);
    
        // Create bullet list
        const list = document.createElement('ul');

        rawText.forEach(text => {
            const li = document.createElement('li');
            li.textContent = text;
            list.appendChild(li);
        });

        container.appendChild(list);
    }  

    function showLoading() {
        loadingDiv.style.display = 'block';
        loadingText.textContent = loadingMessages[loadingMessageIndex];
    
        loadingInterval = setInterval(() => {
            loadingText.style.opacity = 0;
    
            setTimeout(() => {
                loadingMessageIndex = (loadingMessageIndex + 1) % loadingMessages.length;
                loadingText.textContent = loadingMessages[loadingMessageIndex];
                loadingText.style.opacity = 1;
            }, 300);
        }, 2000); // message changes every 2 seconds
    }
    
    function hideLoading() {
        clearInterval(loadingInterval);
        loadingDiv.style.display = 'none';
        loadingMessageIndex = 0;
        loadingText.textContent = "Analyzing job description...";
        loadingText.style.opacity = 1;
    }
});