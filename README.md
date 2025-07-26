# Resume Reviewer AI

A Flask-based web application that analyzes resumes and provides AI-assisted feedback based on job roles, keyword presence, structure, and ATS compatibility.

## Features

- Resume upload (PDF format)
- Job role selection
- Keyword analysis
- ATS compatibility check
- Section-by-section feedback
- Score and suggestions
- History tracking (with login)
- Feedback export

## Tech Stack

- Flask (Python web framework)
- SQLite (Database)
- PyPDF2 (PDF parsing)
- NLTK (NLP for keyword extraction)
- Bootstrap (Frontend styling)
- JavaScript (Frontend interactivity)
- Mock AI integration (No API key required)

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Download NLTK data:
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```
6. Initialize the database:
   ```
   python init_db.py
   ```
7. Run the application:
   ```
   python app.py
   ```

## Project Structure

- `/static` - CSS, JavaScript, and assets
- `/templates` - HTML templates
- `/routes` - Route handlers
- `/utils` - Utility functions for resume parsing and analysis
- `/models` - Database models
- `/uploads` - Directory for uploaded resumes
- `app.py` - Main application file
- `config.py` - Configuration settings
- `init_db.py` - Database initialization script

## Deployment

### Local Development
```
python app.py
```

### Production Deployment (Render)
- Build Command: `pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`
- Start Command: `gunicorn app:app`

## License

MIT 