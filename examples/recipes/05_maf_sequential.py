"""Lab 05 minimal recipe: a two-agent sequential MAF workflow (billable model calls).

The output is guidance for human review; nothing is approved, booked or paid.
"""

import asyncio
import os
import sys

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv


def build_workflow(chat_client):
    analyst = Agent(
        client=chat_client,
        name="PolicyAnalyst",
        instructions="Identify the synthetic policy rules and dates that apply. Cite policy IDs.",
    )
    writer = Agent(
        client=chat_client,
        name="AnswerWriter",
        instructions="Write a short answer from the analysis. Do not approve, book or pay.",
    )
    return SequentialBuilder(participants=[analyst, writer]).build()


async def run(workflow, task: str) -> list[str]:
    result = await workflow.run(task)
    outputs = [str(output) for output in result.get_outputs()]
    if not outputs:
        raise SystemExit("The workflow completed without outputs; no fallback was used.")
    return outputs


async def main() -> None:
    load_dotenv()
    task = " ".join(sys.argv[1:]) or "A KRW 170000 domestic hotel in September 2026: what applies?"
    async with AzureCliCredential() as credential:
        client = FoundryChatClient(
            project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            credential=credential,
        )
        for output in await run(build_workflow(client), task):
            print(output)


if __name__ == "__main__":
    asyncio.run(main())
