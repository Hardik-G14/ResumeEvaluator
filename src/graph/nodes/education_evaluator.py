

from pydantic import BaseModel
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState


class EducationEval(BaseModel):
    degrees: List[str]
    institutions: List[str]
    education_score: float


def education_evaluator(state: ResumeState) -> ResumeState:
    print("Education Evaluator called")

    resume_text = state.get("resume_text", "")

    llm = get_llm().with_structured_output(EducationEval)

    prompt = ChatPromptTemplate.from_template("""
You are an AI resume education evaluator.

Based only on the resume text:
1) Extract the degrees or qualifications mentioned.
2) Identify the institutions/universities attended.
3) Provide an education strength score between 0 and 1.
   Higher score = stronger academic background, relevance, and credibility.

Return ONLY a JSON object with:
- degrees: string[]
- institutions: string[]
- education_score: number

Resume Text:
{resume}
""")

    messages = prompt.format_messages(resume=resume_text)
    result: EducationEval = llm.invoke(messages)

    # state["education_score"] = float(result.education_score)
    # state["degrees"] = result.degrees
    # state["institutions"] = result.institutions

    return {
        "education_score": float(result.education_score),
        "degrees": list(result.degrees or []),
        "institutions": list(result.institutions or []),
    }
