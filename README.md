# AI Resume Analyzer

An AI-powered Resume Analyzer that evaluates resumes against job descriptions to improve ATS compatibility, identify missing skills, and provide recruiter-style recommendations using NLP, semantic similarity, and LLM-based feedback.

---

## Features

- Resume upload (PDF)
- Job Description analysis
- ATS compatibility scoring
- Missing keyword detection
- Resume vs JD skill matching
- Semantic similarity analysis
- AI-generated recruiter feedback
- Resume improvement suggestions
- Interactive dashboard visualizations

---

## Problem Statement

Many candidates submit resumes without knowing:

- whether they pass ATS screening
- which skills recruiters are looking for
- what keywords are missing
- how well their resume matches a target role

This project helps candidates optimize resumes for specific roles using AI-driven analysis.

---

## Demo Workflow

```text
Upload Resume (PDF)
        ↓
Extract Resume Text
        ↓
Upload / Paste Job Description
        ↓
Keyword Extraction (NLP)
        ↓
Semantic Similarity Matching
        ↓
ATS Score Generation
        ↓
LLM-based Recommendations
        ↓
Dashboard Results
```

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### NLP & AI
- spaCy
- Sentence Transformers
- OpenAI API

### Data Processing
- Pandas
- NumPy
- Scikit-learn

### PDF Processing
- PyMuPDF

### Visualization
- Plotly

---

## Project Structure

```text
ai-resume-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── utils/
│   ├── parser.py
│   ├── analyzer.py
│   ├── scorer.py
│
├── screenshots/
├── sample_resumes/
└── assets/
```

---

## Architecture

```text
                +----------------------+
                |   Resume Upload      |
                +----------------------+
                           |
                           v
                +----------------------+
                |   PDF Text Parser    |
                |      (PyMuPDF)       |
                +----------------------+
                           |
                           v
                +----------------------+
                |  Job Description     |
                |      Processing      |
                +----------------------+
                           |
                           v
          +----------------------------------+
          | NLP + Semantic Analysis Engine   |
          | spaCy + Sentence Transformers    |
          +----------------------------------+
                           |
              +------------+------------+
              |                         |
              v                         v
    +------------------+      +-------------------+
    | Keyword Matching |      | Semantic Similar |
    | & ATS Scoring    |      | Resume Fit Score |
    +------------------+      +-------------------+
              |                         |
              +------------+------------+
                           |
                           v
                +----------------------+
                | LLM Recommendations  |
                | (OpenAI / Claude)    |
                +----------------------+
                           |
                           v
                +----------------------+
                | Streamlit Dashboard  |
                +----------------------+
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/ai-resume-analyzer.git
cd ai-resume-analyzer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install spaCy language model:

```bash
python -m spacy download en_core_web_sm
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_api_key_here
```

---

## Run the Application

```bash
streamlit run app.py
```

---

## Example Use Case

### Input
Resume:
- Python
- SQL
- Machine Learning
- LLM Applications

Job Description:
- Python
- LangChain
- Vector Databases
- RAG
- Prompt Engineering

### Output
```text
ATS Score: 78%

Missing Keywords:
- LangChain
- Vector Databases
- RAG

Suggestions:
- Add projects demonstrating retrieval systems
- Include prompt engineering experience
- Improve AI/ML technical keyword visibility
```

---

## Core Modules

### `parser.py`
Responsible for:
- PDF extraction
- text preprocessing
- document loading

### `analyzer.py`
Responsible for:
- keyword extraction
- NLP processing
- semantic similarity analysis

### `scorer.py`
Responsible for:
- ATS scoring
- match percentage
- recommendation logic

---

## Future Improvements

- Resume rewriting suggestions
- Multi-agent recruiter review system
- Interview question generation
- LinkedIn profile analysis
- Resume benchmarking against industry standards
- Skill gap roadmap generation
- DOCX support
- Voice feedback assistant

---

## Screenshots

Add screenshots here after implementation.

Example:

```text
screenshots/
├── dashboard.png
├── ats-score.png
├── recommendation-panel.png
```

---

## Skills Demonstrated

This project demonstrates:

- NLP
- LLM Integration
- Prompt Engineering
- Semantic Search
- Embeddings
- ATS Optimization
- Streamlit App Development
- Python Backend Engineering
- AI Product Design

---

## Author

**Shibani Narendra**

- LinkedIn: your-linkedin-url
- GitHub: your-github-url
