from collections import defaultdict
from typing import Dict, List

from fastapi import WebSocket


class QueueConnectionManager:
    """Keeps track of websocket clients watching a given service's live queue,
    and broadcasts JSON-serializable payloads to all of them when the queue changes."""

    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = defaultdict(list)

    async def connect(self, service_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[service_id].append(websocket)

    def disconnect(self, service_id: str, websocket: WebSocket):
        if websocket in self.active_connections.get(service_id, []):
            self.active_connections[service_id].remove(websocket)
        if not self.active_connections.get(service_id):
            self.active_connections.pop(service_id, None)

    async def broadcast(self, service_id: str, payload: dict):
        stale = []
        for connection in self.active_connections.get(service_id, []):
            try:
                await connection.send_json(payload)
            except Exception:
                stale.append(connection)
        for conn in stale:
            self.disconnect(service_id, conn)


manager = QueueConnectionManager()
