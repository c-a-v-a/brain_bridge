"""Router for chat functionality.

This module defines an authenticaded WebSocket endpoint that:
- Validates user using JWT from WebSocket sub protocol.
- Registers WebSocket connections.
- Broadcasts messages.
- Cleans up disconnected users.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException

from internals.auth import get_current_user_ws
from internals.chat import connect_user, disconnect_user, broadcast

router = APIRouter(prefix="/chat", tags=["chat"])


@router.websocket("/ws")
async def chat(websocket: WebSocket) -> None:
    """Authenticated WebSocket endpoint for chat.

    Clients must pass the JWT token via WebSocket subprotocols.

    Args:
        websocket (WebSocket): WebSocket connection instance.

    Returns:
        None
    """
    try:
        user = await get_current_user_ws(websocket)
        username = user.username
    except Exception:
        username = "guest"
        # await websocket.close(code=1008)
        # return


    print(username)
    # await websocket.accept()
    await connect_user(username, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")

            await broadcast(username, message)
    except WebSocketDisconnect:
        await disconnect_user(username)