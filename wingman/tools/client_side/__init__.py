from langchain.tools import tool
import pyperclip

from .spotify_tool import search_and_play_song, pause_playback, search_uri, play_uri, add_to_queue, skip_track

@tool
def get_age() -> str:
  """Get the user's age"""
  return 19

@tool
def copy2clip(text:str) -> bool:
  """Copy given text to the system clipboard. Returns True if successful"""
  pyperclip.copy(text)
  return True

tools = [get_age, copy2clip, search_and_play_song, pause_playback, search_uri, play_uri, add_to_queue, skip_track]
tool_names = {tool.name:tool for tool in tools}

def execute(name, kwargs):
  return tool_names[name].run(kwargs)