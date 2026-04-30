# Resume Gap Analyzer 


**AI-powered resume gap analyzer using a LangGraph multi-agent system — BIA 810**

Built with Groq · LLaMA-3.3-70b · LangGraph · Streamlit

---

## 1. What the Code Does

Resume Gap Analyzer is a conversational AI chatbot that compares your resume against a specific job description and tells you exactly how well you match.

You upload your resume, paste a job description, and the system gives you:

- **Fit Score (0–100)** — how well your resume matches the job
- **Label** — Strong Fit, Partial Fit, or Not a Fit
- **Missing Skills** — skills the job requires that your resume doesn't show
- **Recruiter Feedback** — honest feedback like a real recruiter would give

- ---

## 2. Code Structure

resume-gap-analyzer/
│
├── pipeline/
│   ├── __init__.py          # AgentState definition (shared state object)
│   ├── extractor.py         # Agent 1 — extracts skills from resume and job description
│   ├── comparator.py        # Agent 2 — compares skill lists, finds matches and gaps
│   ├── scorer.py            # Agent 3 — calls Groq LLM to generate fit score and feedback
│   └── graph.py             # LangGraph wiring — connects the 3 agents in sequence
│
├── sample_data/             # Sample resumes and job descriptions for testing
├── app.py                   # Streamlit frontend — chat UI
├── requirements.txt         # Python dependencies
├── .env.example             # Example environment variables
└── README.md

**Agent 1 — Extractor:** Scans resume and job description for skills using keyword matching.

**Agent 2 — Comparator:** Finds matched and missing skills using pure set logic. No AI.

**Agent 3 — Feedback Agent:** Sends results to Groq LLaMA-3 and gets back a fit score, label, and recruiter feedback in strict JSON.

**graph.py:** Wires all three agents together using LangGraph StateGraph with shared AgentState.

---

## 3. How to Prepare to Run

### Prerequisites
- Python 3.10 or higher
- A free Groq API key from https://console.groq.com

### Step 1 — Clone the repository
```bash
git clone https://github.com/SwathiHS/resume-gap-analyzer.git
cd resume-gap-analyzer
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Set up environment variables
```bash
cp .env.example .env
```
Open `.env` and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

---

## 4. How to Run

```bash
streamlit run app.py
```

Opens at `http://localhost:8501` automatically.

1. Upload your resume as PDF or Word (.docx)
2. Paste the job description
3. Click **Analyze**
4. Get your fit score, missing skills, and feedback instantly

---

## Tech Stack

| Layer | Tool |
|---|---|
| Frontend | Streamlit |
| Agent Orchestration | LangGraph |
| LLM | Groq — LLaMA-3.3-70b-versatile |
| Resume Parsing | pdfplumber (PDF), python-docx (Word) |
| Skill Matching | Python (keyword-based) |
| Fallback Model | Ollama (local) |

---

## Team

Built by **Swathi Holla, Serena Shah, Sofia Udaipurwala, and Phoebe Kershenblatt**
Stevens Institute of Technology — BIA 810 Generative AI, Spring 2026
