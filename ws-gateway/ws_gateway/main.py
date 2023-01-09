import asyncio
import os

import uvicorn
import websockets
from fastapi import WebSocket, FastAPI
from websockets.typing import Subprotocol

application = FastAPI()

STOMP_URL = os.environ.get("STOMP_SERVER_URL")


async def forward(ws: WebSocket, stomp_ws: websockets.WebSocketClientProtocol):
    while True:
        data = await ws.receive_text()
        await stomp_ws.send(data)


async def reverse(ws: WebSocket, stomp_ws: websockets.WebSocketClientProtocol):
    while True:
        data = await stomp_ws.recv()
        await ws.send_text(data)


@application.websocket("/ws")
async def websocket(ws: WebSocket):
    await ws.accept()
    stomp_ws: websockets.WebSocketClientProtocol
    async with websockets.connect(
        STOMP_URL,
        subprotocols=[Subprotocol("v10.stomp"), Subprotocol("v11.stomp")],
    ) as stomp_ws:
        rev_task = asyncio.create_task(reverse(ws, stomp_ws))
        fwd_task = asyncio.create_task(forward(ws, stomp_ws))
        await asyncio.gather(fwd_task, rev_task)


if __name__ == "__main__":
    uvicorn.run("main:application", port=80, host="0.0.0.0", reload=True, log_level="debug")
