import os
# pyrefly: ignore [missing-import]
import google.generativeai as genai
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import logging

load_dotenv(override=True)
logger = logging.getLogger(__name__)

# Configure Gemini API
_model = None
def get_gemini_model():
    """Lazy initialize the Gemini model."""
    global _model
    if _model is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            # Clean the key (remove quotes and whitespace)
            api_key = api_key.strip().strip('"').strip("'")
            try:
                genai.configure(api_key=api_key)
                _model = genai.GenerativeModel('gemini-2.5-flash')
            except Exception as e:
                logger.error(f"Error configuring Gemini: {e}")
                _model = None
    return _model

def calculate_ats_score(keyword_match_ratio, semantic_similarity):
    """
    Calculates a weighted ATS score based on keyword match and semantic fit.
    """
    # Weighting: 40% Keyword Match, 60% Semantic Similarity
    # Clamp inputs to [0, 1]
    kw_ratio = max(0, min(1, keyword_match_ratio))
    sem_sim = max(0, min(1, semantic_similarity))
    
    score = (0.4 * kw_ratio) + (0.6 * sem_sim)
    return round(score * 100, 2)

def generate_recommendations(resume_text, jd_text, missing_keywords):
    """
    Generates AI-powered recommendations using Google Gemini.
    """
    model = get_gemini_model()
    if not model:
        return "Gemini API key not configured or initialization failed. Please add GOOGLE_API_KEY to your .env file."
    
    prompt = f"""
    As an expert HR Recruiter and ATS Specialist, analyze the following Resume against the Job Description.
    
    Resume Text: {resume_text[:2000]}...
    
    Job Description: {jd_text[:2000]}...
    
    Missing Keywords identified: {', '.join(missing_keywords[:20])}
    
    Provide:
    1. A brief summary of how well the resume matches the JD.
    2. 3-5 specific, actionable suggestions to improve the resume for this role.
    3. Advice on where to integrate the missing keywords naturally.
    
    Format the response in clear Markdown.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating recommendations: {e}"
