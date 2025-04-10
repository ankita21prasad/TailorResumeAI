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
    python app.py
    ```

    The backend will run on `http://127.0.0.1:5000`.

4.  **Chrome Extension Setup:**

    *   Open Chrome and go to `chrome://extensions/`.
    *   Enable "Developer mode" in the top right corner.
    *   Click "Load unpacked" and select the `chrome-extension` directory.

## How to Use

1.  Open the TailorAI extension from the Chrome toolbar.
2.  Paste the job description into the "Job Description" textarea.
3.  Upload your resume (PDF or TXT).
4.  Click "Analyze".
5.  Review the matched and missing skills, the AI-generated cover letter, and suggested resume improvements.
6.  Use the copy, download, or email buttons to manage the cover letter.

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
