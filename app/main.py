from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router

from app.core.config import settings
from app.websocket.wsocket import chat_websocket_endpoint
from app.database.db import (
    startup_db_client,
    shutdown_db_client,
    db_connection_status,
)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi.routing import APIWebSocketRoute



API_VERSION = settings.API_V_STR


app = FastAPI()


# Register the startup event handler
@app.on_event('startup')
async def startup_event():
    await startup_db_client(app)
    await db_connection_status()


# Register the shutdown event handler
@app.on_event('shutdown')
async def shutdown_event():
    await shutdown_db_client(app)

# async def lifespan(app: FastAPI):
#     await startup_db_client(app)
#     await db_connection_status()
#     yield
#     await shutdown_db_client(app)




app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# App root
@app.get('/', tags=['Root'])
async def root():
    return {'message': 'Welcome to this fantastic ChatP app! No way!!'}


# Api Routers
app.include_router(api_router, prefix=API_VERSION)


# Register the WebSocket endpoint
app.router.routes.append(APIWebSocketRoute('/ws/chat/{chat_type}/{chat_id}/token={token}', chat_websocket_endpoint))

# routes = [WebSocketRoute(path, endpoint=...), ...]
# app = Starlette(routes=routes)

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logger.error(str(exc))
    return JSONResponse(
        status_code=500,
        content={"message": str(exc), "type": type(exc).__name__}
    )

