import openai
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def calculator(x: float, y: float):
   """Useful for calculations"""
   return f"The sum of {x} and {y} is {x + y}"

@tool
def say_hello(name: str):
   """Useful for greeting people"""
   return f"Hello {name}!"
   

def main():
  model = ChatOpenAI(openai_api_key="anything", openai_api_base="http://0.0.0.0:4000", model="gpt-4-turbo")

  tools = [calculator, say_hello]

  agent_executor = create_react_agent(model, tools)

  print("Welcome! I'm your AI assistant. Type 'quit' to stop use it")
  print("Feel free to ask me any questions.")

  while True:
     user_input = input("\nYou: ").strip()

     if user_input == "quit":
        break
     
     print("\nAssistant: ", end="")
     
     for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=user_input)]}
     ):
        print("Chunk: ", chunk)
        if "agent" in chunk and "messages" in chunk["agent"]:
           for message in chunk["agent"]["messages"]:
              print("Message: ", message)
              print(message.content, end="")
     print()

if __name__ == "__main__":
    main()
