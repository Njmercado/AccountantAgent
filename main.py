from strands import Agent 
from strands.models.ollama import OllamaModel
from tools.categorizer import categorizer
from tools.db import insert_income, insert_outcome, create_user
from strands.tools.executors import SequentialToolExecutor

with open("AGENT.md", "r") as file:
  CONTEXT = file.read()

with open("instructions/instructions.input.md", "r") as file:
  INPUT_INSTRUCTIONS = file.read()

with open("instructions/instructions.output.md", "r") as file:
  OUTPUT_INSTRUCTIONS = file.read()

ollama_model = OllamaModel(
  host="http://localhost:11434",
  model_id="llama3.1:latest",
  temperature=0.2,
  top_p=0.5,
)

agent = Agent(
  tool_executor=SequentialToolExecutor(),
  model=ollama_model,
  tools=[categorizer, insert_income, insert_outcome],
  system_prompt=f"{CONTEXT}\n\n{INPUT_INSTRUCTIONS}",
  structured_output_prompt=OUTPUT_INSTRUCTIONS,
  state={
    "user_id": 1,
    "name": "Juan Perez",
    "email": "usuario@example.com"
  }
)

def main():
  while True:
    user_input = input("\nyou: ")
    if user_input.lower() == 'exit':
      break
    agent(
      f"{user_input}",
    )

if __name__ == "__main__":
  main()
