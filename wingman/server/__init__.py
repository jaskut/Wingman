from fastapi import FastAPI
from langserve import add_routes

from . import ollama, openai

from .. import config

# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

add_routes(
    app,
    ollama.chain,
    path=f"/{config.ollama_endpoint}",
)

add_routes(
    app,
    openai.chain,
    path=f"/{config.openai_endpoint}",
)