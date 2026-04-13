from pipeline import AgentState

def extractor_agent(state: AgentState) -> AgentState:
    resume = state["resume_text"].lower()
    jd = state["jd_text"].lower()

    SKILLS = [
        "python", "sql", "excel", "tableau", "power bi",
        "machine learning", "nlp", "data analysis", "financial modeling",
        "dcf", "valuation", "communication", "leadership", "powerpoint",
        "bloomberg terminal", "accounting", "market research"
    ]

    def extract_skills(text):
        return [s for s in SKILLS if s in text]

    state["resume_profile"] = {
        "skills": extract_skills(resume)
    }
    state["jd_profile"] = {
        "required_skills": extract_skills(jd)
    }

    return state