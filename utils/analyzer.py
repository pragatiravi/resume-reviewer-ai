import re
import os
from .keyword_extractor import match_keywords

def analyze_resume(resume_text, sections, job_role, job_keywords):
    """
    Analyze resume content and provide feedback
    
    Args:
        resume_text (str): Full text of the resume
        sections (dict): Dictionary of resume sections
        job_role (str): Selected job role
        job_keywords (list): List of keywords for the job role
        
    Returns:
        dict: Analysis results including score, feedback, and suggestions
    """
    # Initialize results
    results = {
        "overall_score": 0,
        "summary": "",
        "section_feedback": {},
        "keyword_matches": {},
        "ats_compatible": False,
        "suggestions": []
    }
    
    # Check keyword matches
    keyword_results = match_keywords(resume_text, job_keywords)
    results["keyword_matches"] = keyword_results
    
    # Analyze sections
    section_scores = {}
    section_feedback = {}
    
    # Check if key sections exist and have content
    key_sections = ["summary", "experience", "education", "skills"]
    missing_sections = [s for s in key_sections if not sections.get(s)]
    
    for section_name, content in sections.items():
        # Skip empty sections
        if not content:
            section_scores[section_name] = 0
            section_feedback[section_name] = f"Missing {section_name.capitalize()} section"
            results["suggestions"].append(f"Add a {section_name.capitalize()} section to your resume")
            continue
        
        # Calculate word count
        word_count = len(content.split())
        
        # Section-specific analysis
        if section_name == "header":
            has_email = bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content))
            has_phone = bool(re.search(r'(\+\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', content))
            has_linkedin = "linkedin" in content.lower()
            
            header_score = 0
            header_feedback = []
            
            if has_email:
                header_score += 33
            else:
                header_feedback.append("Missing email address")
                results["suggestions"].append("Add your email address to the header")
                
            if has_phone:
                header_score += 33
            else:
                header_feedback.append("Missing phone number")
                results["suggestions"].append("Add your phone number to the header")
                
            if has_linkedin:
                header_score += 34
            else:
                header_feedback.append("Consider adding LinkedIn profile")
                results["suggestions"].append("Add your LinkedIn profile URL to the header")
            
            section_scores[section_name] = header_score
            section_feedback[section_name] = ", ".join(header_feedback) if header_feedback else "Good header with contact information"
            
        elif section_name == "summary":
            # Check summary length
            if word_count < 30:
                section_scores[section_name] = 50
                section_feedback[section_name] = "Summary is too short"
                results["suggestions"].append("Expand your summary to 3-5 sentences highlighting your experience and skills")
            elif word_count > 150:
                section_scores[section_name] = 70
                section_feedback[section_name] = "Summary is a bit long"
                results["suggestions"].append("Consider shortening your summary to be more concise (3-5 sentences)")
            else:
                section_scores[section_name] = 100
                section_feedback[section_name] = "Good summary length"
                
        elif section_name == "experience":
            # Check for bullet points
            has_bullets = bool(re.search(r'•|\*|-|–', content))
            
            # Check for dates
            has_dates = bool(re.search(r'(19|20)\d{2}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec', content))
            
            exp_score = 0
            exp_feedback = []
            
            if has_bullets:
                exp_score += 50
            else:
                exp_feedback.append("Consider using bullet points to highlight achievements")
                results["suggestions"].append("Use bullet points in your experience section to highlight achievements")
                
            if has_dates:
                exp_score += 50
            else:
                exp_feedback.append("Missing dates for work experience")
                results["suggestions"].append("Add dates to your work experience")
            
            section_scores[section_name] = exp_score
            section_feedback[section_name] = ", ".join(exp_feedback) if exp_feedback else "Good experience section with bullet points and dates"
            
        elif section_name == "education":
            # Simple check for education
            section_scores[section_name] = 100 if word_count > 10 else 50
            section_feedback[section_name] = "Good education section" if word_count > 10 else "Education section could be more detailed"
            
        elif section_name == "skills":
            # Check if skills are relevant to job role
            skill_match_count = 0
            for match in keyword_results["matched"]:
                if match["keyword"] in content.lower():
                    skill_match_count += 1
            
            skill_match_percentage = (skill_match_count / len(keyword_results["matched"]) * 100) if keyword_results["matched"] else 0
            
            if skill_match_percentage < 30:
                section_scores[section_name] = 50
                section_feedback[section_name] = f"Skills section has few relevant keywords for {job_role}"
                results["suggestions"].append(f"Add more skills relevant to {job_role} position")
            else:
                section_scores[section_name] = 100
                section_feedback[section_name] = f"Good skills section with relevant keywords for {job_role}"
                
        else:
            # Default scoring for other sections
            section_scores[section_name] = 80
            section_feedback[section_name] = f"Good {section_name} section"
    
    # Add feedback for missing sections
    for section in missing_sections:
        section_scores[section] = 0
        section_feedback[section] = f"Missing {section.capitalize()} section"
        results["suggestions"].append(f"Add a {section.capitalize()} section to your resume")
    
    # Calculate overall score
    section_weights = {
        "header": 0.05,
        "summary": 0.15,
        "experience": 0.35,
        "education": 0.15,
        "skills": 0.20,
        "projects": 0.05,
        "certifications": 0.025,
        "awards": 0.025
    }
    
    weighted_score = 0
    for section, score in section_scores.items():
        weighted_score += score * section_weights.get(section, 0)
    
    # Add keyword match percentage to score
    keyword_weight = 0.3
    section_weight = 0.7
    
    overall_score = (weighted_score * section_weight) + (keyword_results["match_percentage"] * keyword_weight)
    
    # Check ATS compatibility
    ats_compatible = check_ats_compatibility(resume_text, sections)
    
    # Generate summary feedback
    if overall_score >= 80:
        summary = f"Great resume for {job_role} position! Your resume is well-structured with relevant experience and skills."
    elif overall_score >= 60:
        summary = f"Good resume for {job_role} position, but there's room for improvement. Consider addressing the suggestions provided."
    else:
        summary = f"Your resume needs significant improvements for a {job_role} position. Follow the suggestions to enhance your chances."
    
    # Add ATS feedback to summary
    if ats_compatible:
        summary += " Your resume is ATS-compatible."
    else:
        summary += " Your resume may not be ATS-compatible. Consider simplifying the format."
    
    # Finalize results
    results["overall_score"] = round(overall_score)
    results["summary"] = summary
    results["section_feedback"] = section_feedback
    results["ats_compatible"] = ats_compatible
    
    return results

def calculate_score(sections, keyword_match_percentage):
    """
    Calculate overall resume score
    
    Args:
        sections (dict): Dictionary of section scores
        keyword_match_percentage (float): Percentage of matched keywords
        
    Returns:
        int: Overall score out of 100
    """
    # Define weights for different components
    section_weights = {
        "header": 0.05,
        "summary": 0.15,
        "experience": 0.35,
        "education": 0.15,
        "skills": 0.20,
        "projects": 0.05,
        "certifications": 0.025,
        "awards": 0.025
    }
    
    # Calculate weighted section score
    section_score = 0
    for section, score in sections.items():
        section_score += score * section_weights.get(section, 0)
    
    # Combine section score and keyword match score
    keyword_weight = 0.3
    section_weight = 0.7
    
    overall_score = (section_score * section_weight) + (keyword_match_percentage * keyword_weight)
    
    return round(overall_score)

def check_ats_compatibility(text, sections):
    """
    Check if resume is likely to be ATS compatible
    
    Args:
        text (str): Full resume text
        sections (dict): Dictionary of resume sections
        
    Returns:
        bool: True if resume is likely ATS compatible
    """
    # Check for common ATS issues
    
    # 1. Check for tables (difficult for ATS)
    has_tables = len(re.findall(r'\|\s*\w+\s*\|', text)) > 0
    
    # 2. Check for headers/footers (often missed by ATS)
    # This is a simple heuristic - look for page numbers
    has_page_numbers = bool(re.search(r'Page \d+ of \d+|\d+/\d+', text))
    
    # 3. Check for complex formatting (multiple columns)
    # This is hard to detect from text alone, but we can look for patterns
    has_complex_formatting = False
    
    # 4. Check if key sections are clearly labeled
    has_clear_sections = all(sections.get(s) for s in ["experience", "education", "skills"])
    
    # 5. Check for contact information
    has_contact_info = bool(sections.get("header")) and (
        bool(re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', sections.get("header", ""))) or
        bool(re.search(r'(\+\d{1,3}[-\s]?)?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4}', sections.get("header", "")))
    )
    
    # Calculate ATS compatibility score
    ats_score = 0
    if not has_tables:
        ats_score += 30
    if not has_page_numbers:
        ats_score += 10
    if not has_complex_formatting:
        ats_score += 20
    if has_clear_sections:
        ats_score += 30
    if has_contact_info:
        ats_score += 10
    
    # Resume is considered ATS compatible if score is above threshold
    return ats_score >= 70 