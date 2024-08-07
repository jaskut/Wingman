from fastapi import FastAPI
from langserve import add_routes

from . import ollama, openai

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
    path="/ollama",
)

add_routes(
    app,
    openai.chain,
    path="/openai",
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)