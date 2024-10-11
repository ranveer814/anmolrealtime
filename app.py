import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients = []

# Route to serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html") as f:
        return f.read()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            parsed_data = json.loads(data)
            response_data = {
                "name": parsed_data['name'],
                "uniqueID": parsed_data['uniqueID'],
                "floor": parsed_data['floor'],
                "latitude": parsed_data['latitude'],
                "longitude": parsed_data['longitude']
            }
            await websocket.send_text(json.dumps(response_data))

    except WebSocketDisconnect:
        clients.remove(websocket)
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
