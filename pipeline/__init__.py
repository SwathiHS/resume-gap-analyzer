from typing import TypedDict, Optional

class AgentState(TypedDict):
    # inputs
    resume_text: str
    jd_text: str
    
    # filled by Agent 1 (Extractor)
    resume_profile: Optional[dict]
    jd_profile: Optional[dict]
    
    # filled by Agent 2 (Comparator)
    comparison: Optional[dict]
    
    # retry logic
    retry_count: int
    max_retries: int
    
    # filled by Agent 3 (Feedback)
    fit_score: Optional[int]
    label: Optional[str]
    missing_skills: Optional[list]
    feedback: Optional[str]