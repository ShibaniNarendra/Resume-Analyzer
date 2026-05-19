# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text(file_path_or_bytes):
    """
    Extracts text from a PDF file.
    Supports both file paths and BytesIO (Streamlit upload).
    """
    text = ""
    doc = None
    try:
        if hasattr(file_path_or_bytes, "read"):
            # Ensure we start at the beginning of the stream
            if hasattr(file_path_or_bytes, "seek"):
                file_path_or_bytes.seek(0)
            # It's a file-like object (e.g., from Streamlit)
            doc = fitz.open(stream=file_path_or_bytes.read(), filetype="pdf")
        else:
            # It's a file path
            doc = fitz.open(file_path_or_bytes)
            
        for page in doc:
            text += page.get_text()
            
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""
    finally:
        if doc:
            doc.close()
        
    return text.strip()

def preprocess_text(text):
    """
    Basic text cleaning: remove extra whitespace and normalize.
    """
    if not text:
        return ""
    # Simple normalization: join lines and remove multiple spaces
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return " ".join(lines)
