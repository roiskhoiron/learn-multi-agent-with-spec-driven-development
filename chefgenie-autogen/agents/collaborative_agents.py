from autogen_agentchat.agents import AssistantAgent
from .config import get_model_client

def get_coder_agent():
    model_client = get_model_client()
    return AssistantAgent(
        name="SpecAwareCoder",
        model_client=model_client,
        system_message="""You are an expert Python developer. 
        Generate Python code based on the provided YAML spec.
        - Ensure input/output matches the schema.
        - Include docstrings.
        - Only return the code block.
        - If the SpecValidator provides feedback, fix the code accordingly."""
    )

def get_validator_agent():
    model_client = get_model_client()
    return AssistantAgent(
        name="SpecValidator",
        model_client=model_client,
        system_message="""You are an expert QA engineer.
        Validate the Python code against the YAML spec.
        - Check schemas and test cases.
        - If the code is correct, respond ONLY with 'VALID'.
        - If there are issues, list them clearly so the Coder can fix them."""
    )
