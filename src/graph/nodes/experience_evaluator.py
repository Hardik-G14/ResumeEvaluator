

from pydantic import BaseModel
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState


class ExperienceEval(BaseModel):
    companies: List[str]
    total_experience: float
    experience_score: float
    job_switch_pattern: str
    best_fit_role: str


def experience_evaluator(state: ResumeState) -> ResumeState:
    print("Experience Evaluator called")

    resume_text = state.get("resume_text", "")

    llm = get_llm().with_structured_output(ExperienceEval)

    prompt = ChatPromptTemplate.from_template("""
You are an AI resume experience evaluator and career role matcher.

Based only on the resume text:
1) Identify all **companies or organizations** where the candidate has worked.
2) Estimate the candidate's **total years of professional experience**.
   - Analyze each job experience and calculate the total experience based on start date and end date mentioned
3) Evaluate the **experience score** between 0 and 1.
   - Higher score = longer experience, senior roles, and strong relevance.
4) Summarize the **career pattern**, e.g.:
   - Identify if the candidate has switched jobs multiple times (frequent changes every 1–2 years).
   - Set `job_switch_pattern` = Frequent if frequent switching detected, else Stable.
5) Suggest the **best-fit current role** based on their career trajectory and technologies.
6) Return a **ranked list of companies** the candidate worked for:
   - Prestigious, well-known, or globally reputed companies (Google, Amazon, Microsoft, Meta, Apple, etc.) should appear **first**.
   - Other companies should follow in the order of importance or relevance.
   - Dont add colleges and schools in the list

Return ONLY a JSON object with:
- total_experience: number
- experience_score: number
- job_switch_pattern: string
- best_fit_role: string
- companies: string[]    # Ranked list of companies (prestigious first)

Resume Text:
{resume}""")

    messages = prompt.format_messages(resume=resume_text)
    result: ExperienceEval = llm.invoke(messages)

    return {
        "companies": list(result.companies or []),
        "total_experience": float(result.total_experience),
        "experience_score": float(result.experience_score),
        "job_switch_pattern": str(result.job_switch_pattern),
        "best_fit_role":str(result.best_fit_role)
    }
