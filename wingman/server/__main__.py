from . import *
import uvicorn

uvicorn.run(app, host=config.server_host, port=config.server_port)