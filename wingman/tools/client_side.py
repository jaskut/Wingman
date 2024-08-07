from langchain.tools import tool

@tool
def get_age() -> str:
  """Get the user's age"""
  print("Function call")
  return 19

tools = [get_age]
tool_names = {tool.name:tool for tool in tools}

def execute(name, kwargs):
  return tool_names[name].run(kwargs)