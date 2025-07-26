import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ai_suggestions(resume_text, job_role, keyword_matches, section_feedback):
    """
    Get mock AI-powered suggestions for resume improvement
    
    Args:
        resume_text (str): Full text of the resume
        job_role (str): Selected job role
        keyword_matches (dict): Dictionary with matched and missing keywords
        section_feedback (dict): Dictionary with section feedback
        
    Returns:
        list: List of mock AI-generated suggestions
    """
    # Extract missing keywords
    missing_keywords = [item["keyword"] for item in keyword_matches.get("missing", [])]
    missing_keywords_str = ", ".join(missing_keywords[:5])  # Limit to 5 keywords
    
    # Generate generic suggestions based on missing keywords and section feedback
    suggestions = []
    
    # Add suggestions based on missing keywords
    if missing_keywords:
        suggestions.append(f"Consider adding these keywords to your resume: {missing_keywords_str}")
        
    # Add suggestions based on section feedback
    for section, feedback in section_feedback.items():
        if "missing" in feedback.lower():
            suggestions.append(f"Add a {section.capitalize()} section to your resume")
        elif "too short" in feedback.lower():
            suggestions.append(f"Expand your {section} section with more details")
    
    # Add generic suggestions
    generic_suggestions = [
        f"Tailor your resume specifically for the {job_role} position",
        "Use action verbs to describe your achievements",
        "Quantify your achievements with numbers when possible",
        "Ensure your resume is ATS-compatible by using a clean format",
        "Proofread your resume for grammar and spelling errors"
    ]
    
    # Combine all suggestions
    suggestions.extend(generic_suggestions)
    
    # Limit to 10 suggestions
    return suggestions[:10]

def generate_ai_summary(resume_text, job_role):
    """
    Generate a mock AI summary of the resume
    
    Args:
        resume_text (str): Full text of the resume
        job_role (str): Selected job role
        
    Returns:
        str: Mock AI-generated summary
    """
    # Generate a generic summary based on job role
    return f"This resume appears to be for a {job_role} position. The candidate has included relevant information, but could benefit from more targeted content specific to this role. Consider enhancing keyword relevance and quantifying achievements." 