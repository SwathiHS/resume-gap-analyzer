from typing import TypedDict, NotRequired

class Profile(TypedDict):
    skills: list[str]
    experience: list[str]
    education: list[str]

class Comparison(TypedDict):
    matched_skills: list[str]
    missing_skills: list[str]
    similarity_score: float

class AgentState(TypedDict):
    # inputs
    resume_text: str
    jd_text: str

    # agent outputs
    resume_profile: NotRequired[Profile]
    jd_profile: NotRequired[Profile]
    comparison: NotRequired[Comparison]

    # retry
    retry_count: int
    max_retries: int

    # final output
    fit_score: NotRequired[int]
    label: NotRequired[str]
    missing_skills: NotRequired[list[str]]
    feedback: NotRequired[str]

    # debugging
    current_step: NotRequired[str]
    error: NotRequired[str]
