# 📄 Resume Reviewer AI

An intelligent, AI-powered resume feedback platform built with Flask — designed to help job seekers optimize their resumes for specific roles, ATS systems, and recruiter expectations.

🔗 **Live Demo**: [Resume Reviewer AI on Render](https://resume-reviewer-ai-eidt.onrender.com)

---

## ✨ Features

- 📤 Upload resumes in PDF format  
- 🎯 Select job role for targeted feedback  
- 📊 Analyze structure, keywords, and ATS compatibility  
- 🧠 GPT-powered suggestions using OpenAI API  
- 📈 Section-wise ratings and improvement tips  
- 🧾 Export feedback results (optional enhancement)  
- 👤 User session support for resume history *(future-ready)*

---

## 🛠 Tech Stack

| Backend        | Frontend     | AI/NLP           | Utilities      |
|----------------|--------------|------------------|----------------|
| Flask (Python) | HTML/CSS     | OpenAI GPT-3.5   | PyPDF2         |
| SQLite         | Bootstrap 5  | NLTK (keywords)  | JavaScript     |

---

## 📁 Project Structure

```
resume-reviewer-ai/
├── app.py              # Main Flask app
├── templates/          # HTML templates (Jinja2)
├── static/             # CSS/JS/assets
├── uploads/            # Uploaded resumes
├── models/             # SQLAlchemy models
├── utils/              # Resume analysis logic
├── requirements.txt    # Dependencies
├── Procfile            # Deployment script for Render
├── build.sh            # Setup script for NLTK data
├── .gitignore
└── README.md
```

---

## ⚙️ Local Development Setup

```bash
# 1. Clone the repo
git clone https://github.com/pragatiravi/resume-reviewer-ai.git
cd resume-reviewer-ai

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # For Windows
# or
source venv/bin/activate  # For macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# 5. Run the app
python app.py
```

---

## 🚀 Deployment on Render

| Step                  | Value                                                                 |
|-----------------------|------------------------------------------------------------------------|
| **Build Command**     | `pip install -r requirements.txt && python build.sh`                  |
| **Start Command**     | `gunicorn app:app`                                                    |
| **Runtime (optional)**| `python-3.10` in `runtime.txt`                                        |
| **Environment Var**   | `OPENAI_API_KEY` (from [OpenAI platform](https://platform.openai.com)) |

✅ Tables are auto-created using `db.create_all()` — no manual DB script needed  
✅ Supports free Render instance for demo purposes  

---

## 🖼 Screenshot

> _(Add an actual screenshot below if you’d like to showcase the UI)_

![Resume Reviewer AI Screenshot](https://via.placeholder.com/1000x600.png?text=Upload+a+screenshot+of+your+app+here)

---

## 💡 Future Enhancements

- 🔐 User login + saved resume history  
- 📥 PDF feedback export (with summary)  
- 📊 Resume comparison dashboard  
- 🌐 LinkedIn/GitHub profile enrichment  
- 🔍 Multiple job role matching and suggestions  
- 📶 Resume analytics tracking (submission stats, score trends)

---

## 🧠 Known Limitations

- Currently accepts only `.pdf` resumes  
- Output may vary depending on formatting and content quality  
- Requires valid OpenAI API key for feedback generation

---

## 📜 License

MIT License — free for personal and educational use

---

## 🙌 Author & Credits

Made with ❤️ by [Pragati Ravi](https://github.com/pragatiravi)  
Guided by curiosity, built with AI.

---

> 💬 Found this helpful? Give it a ⭐️ on GitHub, share it with friends, or fork it to build your own version!
