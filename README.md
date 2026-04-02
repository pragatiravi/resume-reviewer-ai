# Resume Reviewer AI 🚀

[![Deploy with Vercel](https://vercel.com/button)](https://resume-reviewer-ai-six.vercel.app)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-blue?style=for-the-badge&logo=vercel)](https://resume-reviewer-ai-six.vercel.app)

Resume Reviewer AI is a professional Flash-based web application designed to help job seekers optimize their resumes. Using Natural Language Processing (NLP) and intelligent analysis, the app provides instant feedback on keyword relevance, ATS (Applicant Tracking System) compatibility, and structural completeness based on specific target job roles.

## ✨ Features

- **Smart Resume Upload**: Seamlessly upload PDF resumes for instant processing.
- **Role-Based Analysis**: Tailor your review by selecting from 18+ industry-standard job roles.
- **ATS Compatibility Score**: Get a clear compatibility rating and overall resume quality score.
- **Keyword Synergy**: Identify missing industry keywords and high-priority skills needed for your target role.
- **Section Insights**: Receive actionable feedback on different resume sections (Summary, Experience, Education, etc.).
- **User Dashboard**: Securely track your upload history and previous analysis results.
- **Professional Export**: Download your analysis report as a clean text file for reference.

## 🛠️ Tech Stack

- **Backend**: Python 3.9+ with Flask
- **NLP/Analysis**: NLTK, scikit-learn, PyPDF2
- **Database**: SQLite (Local) / Compatible with PostgreSQL (Production)
- **Frontend**: Bootstrap 5, Custom Vanilla CSS, JavaScript
- **Deployment**: Vercel Serverless Functions

## 📂 Project Structure

```text
resume-reviewer-ai/
├── app.py              # Flask Entry Point (Vercel Handler)
├── config.py           # Application Configuration
├── requirements.txt    # Production Dependencies
├── vercel.json         # Vercel Deployment Configuration
├── static/             # Assets (CSS, JS, Images)
├── templates/          # Jinja2 HTML Templates
├── routes/             # Blueprint Route Handlers (Auth, Resume, Main)
├── models/             # SQLAlchemy Database Models
├── utils/              # Parsing & Analysis Engines
└── uploads/            # Temporary File Processing
```

## 🚀 Local Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/pragatiravi/resume-reviewer-ai.git
   cd resume-reviewer-ai
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python init_db.py
   ```

5. **Run Application**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

## 🌐 Deployment (Vercel)

This project is optimized for deployment as a Vercel Serverless Function.

### Environment Variables
Set the following variables in the Vercel Dashboard:
- `SECRET_KEY`: A secure random string for session encryption.
- `DATABASE_URL`: (Optional) Connection string for a persistent database (e.g., Vercel Postgres).
- `VERCEL`: Set to `1` (Automatically handled by Vercel).

### Build Configuration
- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt && python -m nltk.downloader punkt stopwords`
- **Root Directory**: `./`

## ⚠️ Known Limitations
- **Stateless Environment**: On Vercel, the local SQLite database in `/tmp` is ephemeral. For persistent user data and history across sessions, it is highly recommended to use a managed database (PostgreSQL).
- **Processing Time**: Resume parsing and AI analysis may experience a slight "cold start" delay during the first request on a serverless instance.

## 🔮 Future Improvements
- Integration with LLMs (OpenAI GPT / Google Gemini) for richer linguistic feedback.
- Persistent production database integration.
- PDF generation for exported feedback reports.
- Support for Word (.docx) file formats.

---
MIT License © 2023 Resume Reviewer AI