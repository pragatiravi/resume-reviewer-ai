import os
import re
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyPDF2
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    text = ""
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    
    return text

def parse_resume_sections(text):
    """
    Parse resume text into sections
    
    Args:
        text (str): Resume text content
        
    Returns:
        dict: Dictionary with section names as keys and content as values
    """
    # Common section headers in resumes
    section_headers = [
        "EDUCATION", "EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT", 
        "SKILLS", "TECHNICAL SKILLS", "PROJECTS", "PROJECT EXPERIENCE",
        "CERTIFICATIONS", "ACHIEVEMENTS", "AWARDS", "PUBLICATIONS",
        "SUMMARY", "PROFESSIONAL SUMMARY", "OBJECTIVE", "PROFILE",
        "CONTACT", "PERSONAL INFORMATION", "REFERENCES", "VOLUNTEER",
        "LANGUAGES", "INTERESTS", "ACTIVITIES"
    ]
    
    # Create regex pattern for section headers
    pattern = r"(?i)^(?:{})(?:\s|:|$)".format("|".join(section_headers))
    
    # Find all potential section headers
    lines = text.split('\n')
    sections = {}
    current_section = "HEADER"
    sections[current_section] = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if line is a section header
        if re.match(pattern, line, re.IGNORECASE):
            # Extract section name (remove any trailing colons)
            section_name = re.sub(r':$', '', line.strip().upper())
            current_section = section_name
            sections[current_section] = []
        else:
            sections[current_section].append(line)
    
    # Convert lists to strings
    for section, content in sections.items():
        sections[section] = '\n'.join(content)
    
    # Map to standardized section names
    standardized_sections = {
        "header": sections.get("HEADER", ""),
        "summary": next((sections[s] for s in ["SUMMARY", "PROFESSIONAL SUMMARY", "OBJECTIVE", "PROFILE"] 
                        if s in sections), ""),
        "experience": next((sections[s] for s in ["EXPERIENCE", "WORK EXPERIENCE", "EMPLOYMENT"] 
                           if s in sections), ""),
        "education": sections.get("EDUCATION", ""),
        "skills": next((sections[s] for s in ["SKILLS", "TECHNICAL SKILLS"] 
                       if s in sections), ""),
        "projects": next((sections[s] for s in ["PROJECTS", "PROJECT EXPERIENCE"] 
                         if s in sections), ""),
        "certifications": sections.get("CERTIFICATIONS", ""),
        "awards": next((sections[s] for s in ["ACHIEVEMENTS", "AWARDS"] 
                       if s in sections), "")
    }
    
    return standardized_sections 