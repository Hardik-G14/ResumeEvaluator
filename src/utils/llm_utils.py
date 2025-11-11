# src/utils/llm_utils.py
from langchain_openai import ChatOpenAI
from src.config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_API_KEY
from langchain_core.prompts import ChatPromptTemplate

def get_llm():
    """
    Returns a configured ChatOpenAI instance with settings
    and API key loaded via dotenv + config.yaml.
    """
    return ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        api_key=LLM_API_KEY
    )

def validate_role(user_role):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("""
    You are a job title validator.
    Check if the following text represents a valid professional job role or title.
    If valid, return:
    "yes - [corrected role title]"
    If not valid, return:
    "no"
    Text: "{user_role}"
    """)

    messages = prompt.format_messages(user_role=user_role)
    response = llm.invoke(messages)
    
    if response.content.startswith("yes"):
        return response.content.split("-", 1)[1].strip().title()

    return False

