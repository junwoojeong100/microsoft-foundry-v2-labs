"""Lab 08 minimal recipe: serve one MAF agent with the Hosted Agent Responses protocol.

The Hosted Agent service is GA; the Python hosting package is prerelease (checked 2026-09-24).
Locally this binds 127.0.0.1 with Azure CLI credentials; in Foundry set WORKSHOP_AUTH_MODE=managed-identity.
"""

import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import AzureCliCredential, ManagedIdentityCredential


def build_server(chat_client) -> ResponsesHostServer:
    agent = Agent(
        client=chat_client,
        name="PolicyGuide",
        instructions="Explain the synthetic travel policies with IDs. Never approve, book or pay.",
    )
    return ResponsesHostServer(agent)


def main() -> None:
    hosted = os.environ.get("WORKSHOP_AUTH_MODE") == "managed-identity"
    credential = ManagedIdentityCredential() if hosted else AzureCliCredential()
    client = FoundryChatClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )
    build_server(client).run(host="0.0.0.0" if hosted else "127.0.0.1")


if __name__ == "__main__":
    main()
