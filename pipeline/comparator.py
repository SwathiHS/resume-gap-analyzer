from . import AgentState

def normalize_skill(skill: str) -> str:
    return skill.strip().lower()

def comparator_agent(state: AgentState) -> AgentState:
    if "resume_profile" not in state or "jd_profile" not in state:
        state["error"] = "Missing resume_profile or jd_profile"
        return state

    resume_skills_raw = state["resume_profile"].get("skills", [])
    jd_skills_raw = state["jd_profile"].get("skills", [])

    resume_skills = {normalize_skill(skill) for skill in resume_skills_raw}
    jd_skills = {normalize_skill(skill) for skill in jd_skills_raw}

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    similarity_score = round((len(matched) / len(jd_skills)) * 100, 1) if jd_skills else 0.0

    state["comparison"] = {
        "matched_skills": matched,
        "missing_skills": missing,
        "similarity_score": similarity_score,
    }

    return state
