from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Allow CORS for the front-end to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, restrict to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected clients (if needed for broadcasting)
clients = []

# WebSocket endpoint to receive and handle data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    
    try:
        while True:
            # Receive the JSON-formatted string from the client (Android app)
            data = await websocket.receive_text()
            
            # Parse the JSON data
            parsed_data = json.loads(data)
            name = parsed_data['name']
            uniqueID = parsed_data['uniqueID']
            floor = parsed_data['floor']
            latitude = parsed_data['latitude']
            longitude = parsed_data['longitude']
            
            # Send back the same data to update the front-end (e.g., the moving dot on the map)
            response_data = {
                "name": name,
                "uniqueID": uniqueID,
                "floor": floor,
                "latitude": latitude,
                "longitude": longitude
            }
            await websocket.send_text(json.dumps(response_data))

    except WebSocketDisconnect:
        clients.remove(websocket)
        print(f"Client {websocket} disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
