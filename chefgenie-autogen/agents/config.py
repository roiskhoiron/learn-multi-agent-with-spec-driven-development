import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

def get_config_list():
    return [
        {
            "model": os.getenv("OPENAI_MODEL", "Torcons"),
            "api_key": os.getenv("OPENAI_API_KEY"),
        }
    ]

llm_config = {
    "config_list": get_config_list(),
    "temperature": 0,
}

def get_model_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file.")
    
    return OpenAIChatCompletionClient(
        model="Torcons",
        api_key=api_key,
        base_url="https://chat.torcons.ai/api/",
        model_info={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
        }
    )
