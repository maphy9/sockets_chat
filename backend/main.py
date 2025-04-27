from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List

app = FastAPI()

# In-memory room store
rooms: Dict[str, List[WebSocket]] = {}

@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str):
    await websocket.accept()
    if room_name not in rooms:
        rooms[room_name] = []
    rooms[room_name].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            for conn in rooms[room_name]:
                if conn != websocket:
                    await conn.send_text(data)
    except WebSocketDisconnect:
        rooms[room_name].remove(websocket)
        if not rooms[room_name]:
            del rooms[room_name]
