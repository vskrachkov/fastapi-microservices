import asyncio
import os

import uvicorn
import websockets
from fastapi import WebSocket, FastAPI
from websockets.typing import Subprotocol

application = FastAPI()

STOMP_URL = os.environ.get("STOMP_SERVER_URL")


@application.websocket("/ws")
async def websocket(client: WebSocket):
    await client.accept()
    broker_ws: websockets.WebSocketClientProtocol
    async with websockets.connect(
        STOMP_URL,
        subprotocols=[Subprotocol("v10.stomp"), Subprotocol("v11.stomp")],
    ) as broker_ws:
        rev_task = asyncio.create_task(reverse(client, broker_ws))
        fwd_task = asyncio.create_task(forward(client, broker_ws))
        await asyncio.gather(fwd_task, rev_task)


async def forward(client: WebSocket, broker: websockets.WebSocketClientProtocol):
    while True:
        data = await client.receive_text()
        await broker.send(data)


async def reverse(client: WebSocket, broker: websockets.WebSocketClientProtocol):
    while True:
        data = await broker.recv()
        await client.send_text(data)


if __name__ == "__main__":
    uvicorn.run("main:application", port=80, host="0.0.0.0", reload=True, log_level="debug")
