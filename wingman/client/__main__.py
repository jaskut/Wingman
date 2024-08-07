from langserve import RemoteRunnable
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import ToolMessage

import asyncio

from ..tools import client_side

url = "http://localhost:8000"
endpoint = "/openai"

openai = RemoteRunnable(url + endpoint)
chat_history = ChatMessageHistory()
#chat_history.add_message(ToolMessage(content="Greeting sent", name="send_greeting", tool_call_id=""))

async def call(chat_history):
  return_value = None
  async for event in openai.astream_events({"chat_history":chat_history.messages}, version="v1"):
    kind = event["event"]
    if kind == "on_chat_model_stream":
      content = event["data"]["chunk"].content
      if content:
        print(content, end="", flush=True)
    #elif kind == "on_chat_model_end":
    #  if event['data']['output']:
    #    message = event['data']['output'].generations[0][0].message.dict()
    #    message.pop('type', 'example')
    #    chat_history.add_message(AIMessage.construct(**message))
    elif kind == "on_tool_start":
      print("--")
      print(
        f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
      )
    elif kind == "on_tool_end":
      print(f"Done tool: {event['name']}")
      print(f"Tool output was: {event['data'].get('output')}")
      print("--")
      #result = event['data']['output']
      #message = chat_history.messages[-1]
      #if 'content' in result:
      #  chat_history.add_message(ToolMessage(content=event['data']['output']['content'], name=message.tool_calls[0]['name'], tool_call_id=message.tool_calls[0]['id']))
      #else:
      #  chat_history.add_message(ToolMessage(content=event['data']['output'], name=message.tool_calls[0]['name'], tool_call_id=message.tool_calls[0]['id']))
    elif kind == "on_chain_end" and event['name'] == endpoint:
      for message in event['data']['output']['messages']:
        if isinstance(message, dict) and message["type"] == "tool":
          message = ToolMessage(**message)
        chat_history.add_message(message)
      return_value = event['data']['output']
  
  return return_value

async def invoke(prompt):
  global chat_history
  chat_history.add_user_message(prompt)
  response = await call(chat_history)
  while 'tool_calls' in response and len(response["tool_calls"]) > 0:
    for tool in response['tool_calls']:
      print("--")
      print(f"Starting tool: {tool['name']} with inputs: {tool['args']}")
      result = client_side.execute(tool['name'], tool['args'])
      print(f"Done tool: {tool['name']}")
      print(f"Tool output was: {result}")
      print("--")
      chat_history.add_message(ToolMessage(content=result, name=tool['name'], tool_call_id=tool['id']))
    response = await call(chat_history)
  

async def main():
  text = input("You: ")
  while not "exit" in text:
    print()
    await invoke(text)
    if "bye" in  text:
      break
    print("\n")    
    text = input("You: ")

asyncio.run(main())
#for chunk in openai.stream({"chat_history":chat_history.messages}):
#  print(chunk)