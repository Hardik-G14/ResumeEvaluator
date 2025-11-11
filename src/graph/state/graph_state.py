from typing import TypedDict
from typing import TypedDict, Optional, List

class ResumeState(TypedDict, total = False):
    pdf_path: str
    resume_text: str
    target_role: str

    ## Sections
    skills_section: str
    experience_section: str
    projects_section: str
    education_section: str
    personal_section: str

    ## Personal
    name: str
    email: str
    phone_number: str
    languages: Optional[List[str]]

    ## Skills Evaluator
    skills_score: int
    matched_skills : Optional[List[str]]
    missing_skills : Optional[List[str]]
    role_inferred: str

    ## Project Evaluator
    project_score: float
    project_tech_stack: Optional[List[str]]
    projects_section: str

    ## Education Evaluator
    education_score: float
    degrees: Optional[List[str]]
    institutions: Optional[List[str]]

    ## Achievements Evaluator
    achievements: List[str]
    achievement_score: float

    ## Experience Evaluator
    experience_score: float
    total_experience: float
    companies: Optional[List[str]]
    job_switch_pattern: str
    best_fit_role: str

    ## Summary
    final_summary: str
    is_suitable: str
    suitability_reason: str

    ## Final score after evaluation
    final_score: float