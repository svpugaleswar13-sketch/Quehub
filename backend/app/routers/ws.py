from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
from app import models
from app.queue_utils import queue_snapshot
from app.ws_manager import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/queue/{service_id}")
async def ws_queue(websocket: WebSocket, service_id: str):
    await manager.connect(service_id, websocket)
    db: Session = SessionLocal()
    try:
        service = db.query(models.Service).filter(models.Service.id == service_id).first()
        if service:
            # Send an initial snapshot immediately on connect
            await websocket.send_json(queue_snapshot(db, service))

        while True:
            # We don't expect messages from the client, but keep the socket
            # open and drain anything it sends (e.g. pings) until it disconnects.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(service_id, websocket)
    finally:
        db.close()
