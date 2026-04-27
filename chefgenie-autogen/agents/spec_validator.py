import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console
from .config import get_model_client

class SpecValidator:
    def __init__(self):
        model_client = get_model_client()
        self.agent = AssistantAgent(
            name="SpecValidator",
            model_client=model_client,
            system_message="""You are an expert QA engineer.
            Your task is to validate Python code against a provided YAML specification.
            Check if the code correctly implements the input/output schemas and test cases.
            If valid, respond with 'VALID'.
            If invalid, provide a detailed list of issues."""
        )

    async def validate(self, spec_content: str, generated_code: str):
        prompt = f"Validate the following Python code against this specification:\n\nSpec:\n{spec_content}\n\nCode:\n{generated_code}"
        termination = MaxMessageTermination(1)
        team = RoundRobinGroupChat([self.agent], termination_condition=termination)
        result = await Console(team.run_stream(task=prompt))
        return result.messages[-1].content
