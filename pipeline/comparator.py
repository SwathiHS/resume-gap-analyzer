from pipeline import AgentState

def comparator_agent(state: AgentState) -> AgentState:
    resume_skills = set(state["resume_profile"]["skills"])
    jd_skills = set(state["jd_profile"]["required_skills"])

    matched = list(resume_skills & jd_skills)
    missing = list(jd_skills - resume_skills)

    coverage = round(len(matched) / len(jd_skills) * 100, 1) if jd_skills else 0.0

    state["comparison"] = {
        "matched_skills": matched,
        "missing_skills": missing,
        "coverage_pct": coverage
    }

    return state