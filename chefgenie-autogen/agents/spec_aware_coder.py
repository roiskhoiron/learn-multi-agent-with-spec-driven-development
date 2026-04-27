import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from .config import get_model_client

class SpecAwareCoder:
    def __init__(self):
        model_client = get_model_client()
        self.agent = AssistantAgent(
            name="SpecAwareCoder",
            model_client=model_client,
            system_message="""You are an expert Python developer. 
            Your task is to generate high-quality, production-ready Python code based on a provided YAML specification.
            Ensure the code follows the input/output schema defined in the spec.
            Include docstrings and basic error handling.
            Only return the code block."""
        )

    async def generate_code(self, spec_content: str):
        prompt = f"Generate Python code for the following specification:\n\n{spec_content}"
        termination = MaxMessageTermination(1)
        team = RoundRobinGroupChat([self.agent], termination_condition=termination)
        result = await team.run(task=prompt)
        return result.messages[-1].content
