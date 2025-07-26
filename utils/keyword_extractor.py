import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

def extract_keywords(text, top_n=30):
    """
    Extract most frequent keywords from text
    
    Args:
        text (str): Text to extract keywords from
        top_n (int): Number of top keywords to return
        
    Returns:
        list: List of top keywords
    """
    # Lowercase the text
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    # Count word frequency
    word_freq = Counter(filtered_tokens)
    
    # Get top N keywords
    top_keywords = [word for word, _ in word_freq.most_common(top_n)]
    
    return top_keywords

def match_keywords(resume_text, job_keywords):
    """
    Match keywords from resume text with job role keywords
    
    Args:
        resume_text (str): Text extracted from resume
        job_keywords (list): List of keywords for the job role
        
    Returns:
        dict: Dictionary with matched and missing keywords
    """
    resume_text = resume_text.lower()
    
    # Match keywords
    matched = []
    missing = []
    
    for keyword in job_keywords:
        # Check if keyword or its variations are in the resume
        if keyword.lower() in resume_text:
            matched.append(keyword)
        else:
            # Check for variations (plural forms, different forms of verbs)
            variations = [
                keyword + 's',
                keyword + 'es',
                keyword + 'ed',
                keyword + 'ing'
            ]
            
            found = False
            for variation in variations:
                if variation.lower() in resume_text:
                    matched.append(keyword)
                    found = True
                    break
            
            if not found:
                missing.append(keyword)
    
    # Calculate match percentage
    total_keywords = len(job_keywords)
    matched_count = len(matched)
    
    match_percentage = (matched_count / total_keywords * 100) if total_keywords > 0 else 0
    
    # Assign importance levels to keywords
    keyword_importance = {}
    for keyword in job_keywords:
        # Determine importance based on position in the list
        # First third are high importance, middle third medium, last third low
        index = job_keywords.index(keyword)
        if index < len(job_keywords) // 3:
            importance = "high"
        elif index < 2 * (len(job_keywords) // 3):
            importance = "medium"
        else:
            importance = "low"
        
        keyword_importance[keyword] = importance
    
    result = {
        "matched": [{"keyword": kw, "importance": keyword_importance[kw]} for kw in matched],
        "missing": [{"keyword": kw, "importance": keyword_importance[kw]} for kw in missing],
        "match_percentage": round(match_percentage, 2)
    }
    
    return result 