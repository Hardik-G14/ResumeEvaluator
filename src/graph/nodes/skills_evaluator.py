# graph/nodes/skills_evaluator.py

from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_utils import get_llm
import json

def skills_evaluator(state: Dict) -> Dict:
    """
    Node C: Evaluates resume skills without a job description.
    Determines the likely target role (e.g., AI Engineer) and 
    scores how complete and relevant the skillset is for that role.
    """

    resume_skills = state.get("skills_section", "")
    if not resume_skills:
        state["skills_score"] = 0.0
        state["matched_skills"] = []
        state["missing_skills"] = []
        state["role_inferred"] = "Unknown"
        return state

    llm = get_llm()

    

    prompt = ChatPromptTemplate.from_template("""
    You are an AI recruitment assistant analyzing a candidate's skills.
    Based only on the given skills, do the following:
    1. Infer the most likely professional role or domain (e.g., AI Engineer, Frontend Developer, DevOps Engineer, Data Scientist).
    2. Identify which critical skills are present and which key skills are missing for that role.
    3. Give an overall skills completeness score between 0 and 1.

    Respond strictly in JSON format like this:
    {{
        "role_inferred": "AI Engineer",
        "matched_skills": ["python", "tensorflow", "machine learning"],
        "missing_skills": ["pytorch", "data preprocessing", "deep learning"],
        "skills_score": 0.82
    }}

    Candidate Skills:
    {resume_skills}
    """)

    messages = prompt.format_messages(resume_skills=resume_skills)
    response = llm.invoke(messages)

    try:
        data = json.loads(response.content)
    except Exception:
        data = {
            "role_inferred": "Unknown",
            "matched_skills": [],
            "missing_skills": [],
            "skills_score": 0.0
        }

    state["role_inferred"] = data.get("role_inferred", "Unknown")
    state["skills_score"] = data.get("skills_score", 0.0)
    state["matched_skills"] = data.get("matched_skills", [])
    state["missing_skills"] = data.get("missing_skills", [])

    return state
