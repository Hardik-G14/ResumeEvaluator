from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState

class SummaryEval(BaseModel):
    summary: str
    suitable: str
    reason: str

def summarizer(state: ResumeState) -> ResumeState:
    print("Summarizer called")

    llm = get_llm().with_structured_output(SummaryEval)

    prompt = ChatPromptTemplate.from_template("""
You are an AI resume evaluator.
Given the candidate's details and target role, provide:
1) A short 3–4 line professional summary.
2) A suitability verdict ("Yes" or "No").
3) A brief reason (1–2 lines).

Candidate Profile:
Skills: {skills}
Education: {education}
Experience: {experience} years
Experience Score: {experience_score}
Job Hop Flag: {job_hop_flag}
Career Pattern: {career_pattern}
Previous Companies: {companies}

Target Role: {target_role}

Return JSON with:
- summary: string
- suitable: string ("Yes" or "No")
- reason: string
""")
    result = llm.invoke(prompt.format_messages(
        skills=state.get("matched_skills", []),
        education=state.get("education", []),
        experience=state.get("total_experience", 0),
        experience_score=state.get("experience_score", 0),
        job_hop_flag=state.get("job_hop_flag", False),
        career_pattern=state.get("job_switch_pattern", ""),
        companies=state.get("companies", []),
        target_role=state.get("target_role", "Unknown Role")
    ))

    return {
        "final_summary": result.summary,
        "is_suitable": result.suitable,
        "suitability_reason": result.reason
    }
