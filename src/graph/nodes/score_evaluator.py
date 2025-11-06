

from src.graph.state.graph_state import ResumeState
from src.config.settings import (
    WEIGHT_SKILLS,
    WEIGHT_EXPERIENCE,
    WEIGHT_PROJECTS,
    WEIGHT_EDUCATION,
)

def score_evaluator(state: ResumeState) -> ResumeState:
    print("Score Evaluator called")


    skills = float(state.get("skills_score", 0.0))
    experience = float(state.get("experience_score", 0.0))
    project = float(state.get("project_score", 0.0))
    education = float(state.get("education_score", 0.0))

    
    final_score = (
        WEIGHT_SKILLS * skills +
        WEIGHT_EXPERIENCE * experience +
        WEIGHT_PROJECTS * project +
        WEIGHT_EDUCATION * education
    )

    
    state["final_score"] = round(final_score, 3)
    print(f"[score_evaluator] → Final Score: {state['final_score']}")

    return state
