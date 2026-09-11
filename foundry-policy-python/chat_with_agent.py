import os
from pathlib import Path

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential


ENV_FILE = Path(__file__).resolve().parent / ".env"

load_dotenv(ENV_FILE)

PROJECT_ENDPOINT = os.getenv("PROJECT_ENDPOINT")
AGENT_NAME = os.getenv("AGENT_NAME")


if not PROJECT_ENDPOINT:
    raise RuntimeError("PROJECT_ENDPOINT is missing from the .env file.")

if not AGENT_NAME:
    raise RuntimeError("AGENT_NAME is missing from the .env file.")


project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client(
    agent_name=AGENT_NAME
)

conversation = openai.conversations.create()

print("Company Policy Assistant")
print("Type 'exit' to stop.\n")


while True:
    question = input("You: ").strip()

    if question.lower() in ["exit", "quit", "stop", "bye"]:
        print("Goodbye.")
        break

    if not question:
        continue

    response = openai.responses.create(
        conversation=conversation.id,
        input=question,
    )

    print(f"\nAgent: {response.output_text}\n")
