from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# To allow frontend to access backend via browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket route for real-time data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data_json = json.loads(data)
        unique_id = data_json["uniqueID"]
        latitude = data_json["latitude"]
        longitude = data_json["longitude"]
        floor = data_json["floor"]

        # Send the latest location data back to the client
        await websocket.send_text(json.dumps(data_json))

# Route to serve the index.html directly
@app.get("/", response_class=HTMLResponse)
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Real-Time Tracking</title>
        <style>
            #map { height: 100vh; width: 100%; }
        </style>
        <script>
            var ws = new WebSocket("wss://anmolrealtime.onrender.com/ws");
            ws.onmessage = function(event) {
                var data = JSON.parse(event.data);
                var latitude = data.latitude;
                var longitude = data.longitude;
                console.log("Latitude: " + latitude + ", Longitude: " + longitude);
                // Update the dot position on the map
                updateDotPosition(latitude, longitude);
            };

            function updateDotPosition(latitude, longitude) {
                var dot = document.getElementById("dot");
                // Convert latitude and longitude to X, Y coordinates based on your map's dimensions
                // Adjust the values based on your map's coordinates
                var x = (longitude - 75.8465) * 1000;  // Example conversion factor
                var y = (30.9015 - latitude) * 1000;   // Example conversion factor
                dot.style.left = x + "px";
                dot.style.top = y + "px";
            }
        </script>
    </head>
    <body>
        <div id="map">
            <img src="/map" alt="Map" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
            <div id="dot" style="position: absolute; width: 10px; height: 10px; background-color: blue; border-radius: 50%;"></div>
        </div>
    </body>
    </html>
    """
    return html_content

# Serve the image directly from the root
@app.get("/map")
async def get_map_image():
    return FileResponse("mapanmol.jpg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
