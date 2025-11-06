from langgraph.graph import StateGraph, START, END

from src.graph.state.graph_state import ResumeState
from src.graph.nodes.pdf_loader import pdf_loader
from src.graph.nodes.skills_evaluator import skills_evaluator
from src.graph.nodes.personal_evaluator import personal_info_extractor
from src.graph.nodes.project_evaluator import project_evaluator
from src.graph.nodes.education_evaluator import education_evaluator
from src.graph.nodes.score_evaluator import score_evaluator

def create_graph():
    graph = StateGraph(ResumeState)

    graph.add_node("pdf_loader", pdf_loader)
    graph.add_node("skills_evaluator", skills_evaluator)
    graph.add_node("project_evaluator", project_evaluator)
    graph.add_node("score_aggregator", score_evaluator)

    graph.add_node("personal_info_evaluator", personal_info_extractor)
    graph.add_node("education_evaluator", education_evaluator)

    graph.add_edge(START, "pdf_loader")
    graph.add_edge("pdf_loader", "skills_evaluator")
    graph.add_edge("pdf_loader", "personal_info_evaluator")
    graph.add_edge("pdf_loader", "project_evaluator")
    graph.add_edge("pdf_loader", "education_evaluator")
    graph.add_edge("skills_evaluator", "score_evaluator")
    graph.add_edge("project_evaluator", "score_evaluator")
    graph.add_edge("education_evaluator", "score_evaluator")
    graph.add_edge("score_evaluator", END)
    compile_graph = graph.compile()
    
    return compile_graph