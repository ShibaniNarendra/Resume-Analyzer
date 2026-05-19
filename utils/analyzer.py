# pyrefly: ignore [missing-import]
import spacy
# pyrefly: ignore [missing-import]
from sentence_transformers import SentenceTransformer, util

# Global variables for models (lazy-loaded)
_nlp = None
_model = None

def get_spacy_model():
    """Lazy load the spaCy model."""
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if model not downloaded
            _nlp = None
    return _nlp

def get_sentence_transformer():
    """Lazy load the Sentence Transformer model."""
    global _model
    if _model is None:
        try:
            # 'all-MiniLM-L6-v2' is fast and effective for similarity
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception:
            _model = None
    return _model

def extract_keywords(text):
    """
    Extracts keywords (nouns and proper nouns) from text using spaCy.
    """
    nlp = get_spacy_model()
    if not nlp or not text:
        return []
    
    doc = nlp(text.lower())
    # Extracting nouns, proper nouns and adjectives as potential keywords
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 1]
    return list(set(keywords))

def get_semantic_similarity(text1, text2):
    """
    Calculates semantic similarity between two texts using Sentence Transformers.
    """
    model = get_sentence_transformer()
    if not model or not text1 or not text2:
        return 0.0
    
    # Compute embeddings
    embeddings1 = model.encode(text1, convert_to_tensor=True)
    embeddings2 = model.encode(text2, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    return float(cosine_scores[0][0])

def match_keywords(resume_keywords, jd_keywords):
    """
    Compares resume keywords against JD keywords.
    Returns matched keywords and missing keywords.
    """
    resume_set = set(resume_keywords)
    jd_set = set(jd_keywords)
    
    matched = list(resume_set.intersection(jd_set))
    missing = list(jd_set.difference(resume_set))
    
    return matched, missing
