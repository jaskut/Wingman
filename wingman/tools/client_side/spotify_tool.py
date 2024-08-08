import spotipy
from spotipy.oauth2 import SpotifyOAuth
from langchain.tools import tool

from typing import List

from ... import commands

import time

scope = ["user-read-playback-state", "user-modify-playback-state"]

client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

@tool
def search_and_play_song(query: str) -> dict:
  """Search the given query and play the result on the Spotify App.
  The returned dictionary contains details of the search results and the device it's played on."""
  if len(client.devices()['devices']) == 0:
    commands.open_app("Spotify")
    for i in range(20):
      if len(client.devices()['devices']) > 0:
        break
      time.sleep(0.5)
  if len(client.devices()['devices']) == 0:
    return {"error": "Failed to open application."}
  device = client.devices()['devices'][0]
  result = client.search(query, 1, type="track")
  client.start_playback(device_id=device["id"], uris=[result["tracks"]["items"][0]["uri"]])
  return {"track": result["tracks"]["items"][0], "device": device}

@tool
def search_uri(query: str, type: str = "track,album") -> dict:
  """Search the given query and return the result as a dict.
  type - the types of items to return. One or more of 'artist', 'album',
  'track', 'playlist', 'show', and 'episode'. If multiple types are desired, 
  pass in a comma separated string; e.g., 'track,album,episode'."""
  return client.search(query, 2, type=type)

@tool
def play_uri(context_uri: str = None, uris: List[str] = None) -> dict:
  """Plays the given uris in the Spotify app.
  Provide a context_uri to start playback of an album, artist, or playlist.
  Provide a uris list to start playback of one or more tracks.
  Provide no uris to resume the playback of the currently playing song.
  Returns a dict containing information on the device the uri is being played on."""
  if len(client.devices()['devices']) == 0:
    commands.open_app("Spotify")
    for i in range(20):
      if len(client.devices()['devices']) > 0:
        break
      time.sleep(0.5)
  if len(client.devices()['devices']) == 0:
    return {"error": "Failed to open application."}
  device = client.devices()['devices'][0]
  client.start_playback(device_id=device["id"], context_uri=context_uri, uris=uris)
  return device

@tool
def pause_playback() -> dict:
  """Pause the playback on the Spotify App.
  The returned dictionary contains details of the search results and the device it's played on."""
  result = client.current_playback()
  if result["is_playing"]:
    client.pause_playback()
  return {"track": result["item"], "device": result['device']}

@tool
def add_to_queue(uri: str) -> bool:
  """Add given track uri to the end of the queue.
  Returns true if successful"""
  try:
    client.add_to_queue(uri)
    return True
  except Exception:
    return False
  
@tool
def skip_track() -> dict:
  """Skip the playback to the next track.
  Returns information on the new track and playback status"""
  try:
    client.next_track()
    return client.current_playback()
  except Exception:
    return {"error": "Failed to skip to next track"}

if __name__ == "__main__":
  print(play_uri.run({}))