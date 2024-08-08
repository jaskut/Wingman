import platform
import os

system = platform.system()
def open_app(name):
  if system == 'Darwin':
    os.system(f"open /Applications/{name}.app")

if __name__ == "__main__":
  open_app("Spotify")