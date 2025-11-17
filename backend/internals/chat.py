"""WebSocket connection manager for handling chat functionality.

This module provides utility functions for:
- Accepting WebSocket connections.
- Removing users from the connection pool.
- Broadcasting JSON-formatted chat messages to all connected users.

For now the `active_connections` dictionary holds the map of all connected
users. This will be later changed to different approach, as we scale the
application and create multiple chatrooms.
"""

import json

from fastapi import WebSocket
from typing import Dict

# Map of username->WebSocket
active_connections: Dict[str, WebSocket] = {}


async def connect_user(username: str, websocket: WebSocket) -> None:
    """Accept a WebSocket connection and register the user.

    Args:
        username (str): The username associated with the client.
        websocket (WebSocket): The WebSocket instance for the user.

    Returns:
        None
    """
    await websocket.accept()

    active_connections[username] = websocket


async def disconnect_user(username: str) -> None:
    """Remove the user's WebScoket connection from the active pool.

    Args:
        username (str): The username whose connection should be removed.

    Returns:
        None
    """
    active_connections.pop(username, None)


async def broadcast(username: str, message: str) -> None:
    """Broadcast a JSON-formatted message to all connected users.

    Args:
        username (str): The username of the sender.
        message (str): The text message to broadcast.

    Returns:
        None

    Example Payload:
        {
            "username": "John",
            "message": "Hello world!" 
        }
    """
    payload = {
      "username": username,
      "message": message
    }

    for ws in active_connections.values():
        await ws.send_text(json.dumps(payload))