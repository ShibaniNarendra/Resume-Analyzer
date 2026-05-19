# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go
import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Import utility functions
try:
    from utils.parser import extract_text, preprocess_text
    from utils.analyzer import extract_keywords, get_semantic_similarity, match_keywords
    from utils.scorer import calculate_ats_score, generate_recommendations
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

load_dotenv(override=True)

st.set_page_config(page_title="AI Resume Analyzer", layout="wide", page_icon="📄")

# Custom CSS for a more polished look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 AI Resume Analyzer")
st.markdown("Optimize your resume for ATS compatibility and get expert AI feedback.")

# Sidebar for configuration and info
with st.sidebar:
    st.header("About")
    st.info("This tool uses NLP (spaCy) and Semantic Similarity (Sentence Transformers) to analyze your resume against a Job Description. Recommendations are powered by Google Gemini.")
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.warning("⚠️ GOOGLE_API_KEY not found in .env file. AI recommendations will be disabled.")
    else:
        st.success("✅ Gemini API Key detected.")
        if api_key.startswith((" ", "\"", "'")) or api_key.endswith((" ", "\"", "'")):
             st.info("💡 Note: Your API key has leading/trailing whitespace or quotes. I will automatically clean it, but you should check your .env file.")

# Main layout
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("1. Upload Resume")
    resume_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])

with col_right:
    st.subheader("2. Job Description")
    jd_text = st.text_area("Paste the Job Description here", height=200)

if st.button("Analyze Resume"):
    if resume_file and jd_text:
        with st.spinner("🔍 Analyzing your resume... This may take a moment."):
            # 1. Parsing
            resume_raw_text = extract_text(resume_file)
            resume_text = preprocess_text(resume_raw_text)
            clean_jd_text = preprocess_text(jd_text)
            
            if not resume_text:
                st.error("Could not extract text from the resume. Please ensure it's a valid PDF.")
            else:
                # 2. NLP Analysis
                resume_keywords = extract_keywords(resume_text)
                jd_keywords = extract_keywords(clean_jd_text)
                
                matched_keywords, missing_keywords = match_keywords(resume_keywords, jd_keywords)
                
                # 3. Semantic Similarity
                similarity_score = get_semantic_similarity(resume_text, clean_jd_text)
                
                # 4. ATS Scoring
                keyword_match_ratio = len(matched_keywords) / len(jd_keywords) if jd_keywords else 0
                ats_score = calculate_ats_score(keyword_match_ratio, similarity_score)
                
                # --- RESULTS DASHBOARD ---
                st.divider()
                st.header("📊 Analysis Dashboard")
                
                # Top Row: Score and Metrics
                m_col1, m_col2, m_col3 = st.columns([2, 1, 1])
                
                with m_col1:
                    # Gauge Chart for ATS Score
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = ats_score,
                        title = {'text': "ATS Compatibility Score"},
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "#007bff"},
                            'steps': [
                                {'range': [0, 40], 'color': "#ff4b4b"},
                                {'range': [40, 70], 'color': "#ffa500"},
                                {'range': [70, 100], 'color': "#28a745"}
                            ],
                        }
                    ))
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                with m_col2:
                    st.metric("Keyword Match", f"{int(keyword_match_ratio * 100)}%")
                    st.write(f"**{len(matched_keywords)}** keywords found out of **{len(jd_keywords)}** required.")
                
                with m_col3:
                    st.metric("Semantic Fit", f"{int(similarity_score * 100)}%")
                    st.write("Measures how well your experience conceptually aligns with the role.")

                # Middle Row: Keywords
                k_col1, k_col2 = st.columns(2)
                
                with k_col1:
                    st.subheader("✅ Matched Keywords")
                    if matched_keywords:
                        st.write(", ".join(matched_keywords[:30]))
                    else:
                        st.write("No direct keyword matches found.")
                        
                with k_col2:
                    st.subheader("❌ Missing Keywords")
                    if missing_keywords:
                        st.write(", ".join(missing_keywords[:30]))
                        st.warning("Consider incorporating these into your resume.")
                    else:
                        st.success("You have all the key terms covered!")

                # Bottom Section: AI Recommendations
                st.divider()
                st.subheader("🤖 AI-Powered Recommendations")
                recommendations = generate_recommendations(resume_text, clean_jd_text, missing_keywords)
                st.markdown(recommendations)
                
                st.success("Analysis complete!")
    else:
        st.error("Please provide both a resume file and a job description.")

# Footer
st.divider()
st.caption("AI Resume Analyzer | Built with Streamlit, spaCy, and Gemini")
