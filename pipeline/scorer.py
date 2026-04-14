import os
import json
import re
import requests
from dotenv import load_dotenv
from pipeline import AgentState

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = """
You are a senior recruiter for business and finance roles.
Given a resume, job description, and skill comparison, respond ONLY with valid JSON:
{
  "fit_score": <int 0-100>,
  "label": <"Strong Fit" | "Partial Fit" | "Not a Fit">,
  "missing_skills": [<string>],
  "feedback": <string — 2-3 sentences of honest recruiter feedback>
}
No markdown, no extra text, just JSON.
"""

def feedback_agent(state: AgentState) -> AgentState:
    comparison = state["comparison"]

    user_prompt = f"""
RESUME: {state["resume_text"]}
JOB DESCRIPTION: {state["jd_text"]}
MATCHED SKILLS: {comparison["matched_skills"]}
MISSING SKILLS: {comparison["missing_skills"]}
COVERAGE: {comparison["coverage_pct"]}%
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }
    )

    raw = response.json()["choices"][0]["message"]["content"]
    clean = re.sub(r"```json|```", "", raw).strip()
    result = json.loads(clean)

    state["fit_score"] = result["fit_score"]
    state["label"] = result["label"]
    state["missing_skills"] = result["missing_skills"]
    state["feedback"] = result["feedback"]

    state["retry_count"] = state.get("retry_count", 0) + 1
    return state