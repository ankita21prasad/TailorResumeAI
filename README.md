# TailorAI - Smart Job Application Helper

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone [repository-url]
    cd tailorai-extension
    ```

2.  **Backend Setup (Python):**

    *   Create a virtual environment:

        ```bash
        cd backend
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```

    *   Install dependencies:

        ```bash
        pip install -r requirements.txt
        ```

    *   Set up your Gemini API key:

        *   Create a `.env` file in the `backend` directory.
        *   Add your API key:

            ```
            GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
            ```

3.  **Run the Backend:**

    ```bash
    python main.py
    ```

    The backend will run on `http://127.0.0.1:5000`.

4.  **Chrome Extension Setup:**

    *   Open Chrome and go to `chrome://extensions/`.
    *   Enable "Developer mode" in the top right corner.
    *   Click "Load unpacked" and select the `chrome-extension` directory.

## How to Use

1.  **Open the TailorAI extension:** Click on the TailorAI icon in your Chrome toolbar.
2.  **Enter Your Preferences:** Fill out the preference fields to tailor the output to your liking.
    *   **Preferred Resume Tone:** Choose the desired tone for your resume (e.g., Technical, Formal, Friendly).
    *   **Highlight Focus:** Specify what you want your resume to emphasize (e.g., Achievements, Skills, Projects).
    *   **Experience Level:** Indicate your current experience level (e.g., Entry, Mid, Senior).
    *   **Style Preferences:** Describe your preferred resume styles (e.g., Clean formatting, Quantified results, Buzzwords).
3.  **Paste the Job Description:** Copy and paste the job description into the "Job Description" textarea.
4.  **Upload Your Resume:** Upload your resume file (PDF, TXT or JSON format).
5.  **Click "Analyze":** Initiate the analysis process. A loading message will appear while the extension processes your data.
6.  **Review the Results:** Once the analysis is complete, review the following:
    *   **Matched Skills:** Skills from your resume that align with the job description.
    *   **Missing Skills:** Skills listed in the job description that are not found in your resume.
    *   **AI-Generated Cover Letter:** A personalized cover letter tailored to the job and your qualifications.
    *   **Resume Improvement Suggestions:** Actionable suggestions to improve your resume and better align it with the job description (displayed as bullet points).
7.  **Manage the Cover Letter:**
    *   Use the "Copy" button to copy the cover letter to your clipboard.
    *   Use the "Download" button to download the cover letter as a text file.
    *   Use the "Email" button to open your email client with the cover letter in the body.

## Gemini API Setup

1.  **Get an API Key:**

    *   Go to the [Google AI Studio](https://makersuite.google.com/app/apikey) to obtain an API key.
    *   Make sure to enable the Gemini API for your project.

2.  **Set the API Key:**

    *   As mentioned in the Backend Setup, store your API key in the `.env` file.

## Sample Files for Testing

*   You can place sample resume and job description files in the `backend` directory for testing purposes.  Adjust the file paths in the `app.py` and `popup.js` files accordingly if you want to load them by default.

## UI Design Notes

*   The UI is designed with a card-based layout.
*   A dark mode toggle can be added in the `popup.html` and `popup.css` files.
*   Feedback buttons (👍 / 👎) can be added to the generated content section.

## Troubleshooting

*   **Gemini API Key Issues:** Ensure your Gemini API key is correctly set in the `.env` file.
*   **Backend Not Running:** Make sure the Flask backend is running before using the extension.
*   **Extension Not Loading:** Double-check that you have loaded the extension correctly in Chrome's developer mode.
*   **CORS Errors:** If you encounter CORS errors, ensure that the Flask backend is configured to allow cross-origin requests (CORS is enabled).