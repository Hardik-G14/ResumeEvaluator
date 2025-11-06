# src/config/settings.py
import os
import yaml
from dotenv import load_dotenv

# 1️⃣ Load environment variables from .env
load_dotenv()

# 2️⃣ Load YAML config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def load_config(path=CONFIG_PATH):
    with open(path, "r") as file:
        return yaml.safe_load(file)

CONFIG = load_config()

# 3️⃣ Read LLM config
LLM_PROVIDER = CONFIG["llm"]["provider"]
LLM_MODEL = CONFIG["llm"]["model"]
LLM_TEMPERATURE = CONFIG["llm"]["temperature"]
LLM_MAX_TOKENS = CONFIG["llm"]["max_tokens"]

# This is where .env and yaml connect 👇
LLM_API_KEY = os.getenv(CONFIG["llm"]["api_key_env"])  # → "OPENAI_API_KEY"
if LLM_API_KEY is None:
    raise ValueError("LLM API key not found in environment variables.")


