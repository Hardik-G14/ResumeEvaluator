

from pydantic import BaseModel
from typing import List

class ProjectEval(BaseModel):
    projects_summary: List[str]
    tech_stack: List[str]
    project_score: float


from langchain_core.prompts import ChatPromptTemplate
from src.utils.llm_utils import get_llm
from src.graph.state.graph_state import ResumeState
from .project_evaluator import ProjectEval 


def project_evaluator(state: ResumeState) -> ResumeState:
    print("Project Evaluator called")

  
    resume_text = state.get("projects_section") or state["resume_text"]

    llm = get_llm().with_structured_output(ProjectEval)  

    prompt = ChatPromptTemplate.from_template("""
You are an AI recruitment assistant evaluating the candidate's project experience.

Based only on the resume text:
1) Identify the key projects the candidate worked on (summarize them).
2) Extract the technologies / tools used across these projects.
3) Provide a project relevance score between 0 and 1. 
   - Higher = strong, relevant, clear project experience
   - Lower = weak or unclear project work

Return ONLY a JSON object with keys:
- projects_summary: string[]
- tech_stack: string[]
- project_score: number

Candidate Resume:
{resume}
""")

    messages = prompt.format_messages(resume=resume_text)
    result: ProjectEval = llm.invoke(messages)


    state["project_score"] = float(result.project_score)
    state["projects_section"] = "\n".join(result.projects_summary)
    state["project_tech_stack"] = list(result.tech_stack)

    return state
