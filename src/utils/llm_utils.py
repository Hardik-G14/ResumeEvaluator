# src/utils/llm_utils.py
from langchain_openai import ChatOpenAI
from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_API_KEY

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
