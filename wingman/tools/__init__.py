from . import client_side, server_side
tools = client_side.tools + server_side.tools

def is_client_side(name):
  return name in client_side.tool_names.keys()