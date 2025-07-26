import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-development-only'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///resume_reviewer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'pdf'}
    
    # Job roles for dropdown
    JOB_ROLES = [
        "Data Scientist",
        "Data Analyst",
        "Machine Learning Engineer",
        "Software Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Full Stack Developer",
        "DevOps Engineer",
        "Cloud Engineer",
        "UI/UX Designer",
        "Product Manager",
        "Project Manager",
        "Business Analyst",
        "Marketing Specialist",
        "Sales Representative",
        "Financial Analyst",
        "Human Resources Specialist"
    ]
    
    # Keywords by job role
    JOB_ROLE_KEYWORDS = {
        "Data Scientist": [
            "python", "r", "sql", "machine learning", "deep learning", "statistics", 
            "data visualization", "pandas", "numpy", "scikit-learn", "tensorflow", 
            "pytorch", "tableau", "power bi", "big data", "hadoop", "spark", 
            "data mining", "data modeling", "nlp", "computer vision", "a/b testing"
        ],
        "Software Engineer": [
            "java", "python", "c++", "javascript", "go", "rust", "algorithms", 
            "data structures", "object-oriented", "design patterns", "api", 
            "microservices", "distributed systems", "cloud", "aws", "azure", 
            "gcp", "docker", "kubernetes", "ci/cd", "testing", "git"
        ],
        "Frontend Developer": [
            "html", "css", "javascript", "typescript", "react", "vue", "angular", 
            "responsive design", "sass", "less", "webpack", "babel", "redux", 
            "ui/ux", "accessibility", "seo", "progressive web apps", "spa", 
            "jest", "cypress", "figma", "adobe xd"
        ],
        "Backend Developer": [
            "python", "java", "c#", "node.js", "go", "ruby", "php", "sql", "nosql", 
            "mongodb", "postgresql", "mysql", "redis", "api", "rest", "graphql", 
            "microservices", "docker", "kubernetes", "aws", "azure", "gcp", "orm"
        ],
        "Product Manager": [
            "product strategy", "roadmap", "user stories", "market research", 
            "competitive analysis", "agile", "scrum", "kanban", "stakeholder management", 
            "user experience", "a/b testing", "metrics", "kpis", "product lifecycle", 
            "prioritization", "mvp", "product launch", "jira", "confluence"
        ],
        "Cloud Engineer": [
            "aws", "azure", "gcp", "cloud architecture", "iaas", "paas", "saas", 
            "terraform", "cloudformation", "kubernetes", "docker", "serverless", 
            "lambda", "s3", "ec2", "rds", "dynamodb", "vpc", "security", "ci/cd", 
            "monitoring", "logging", "cost optimization"
        ]
    }
    
    # Default keywords for roles not specifically defined
    DEFAULT_KEYWORDS = [
        "communication", "teamwork", "leadership", "problem solving", 
        "critical thinking", "time management", "project management", 
        "analytical skills", "attention to detail", "creativity"
    ]
    
    # Resume sections to analyze
    RESUME_SECTIONS = [
        "header", "summary", "experience", "education", 
        "skills", "projects", "certifications", "awards"
    ] 