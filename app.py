from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# CORS middleware setup to allow communication between different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your front-end domain for security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # You can broadcast this to multiple connected clients or just send it back
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
