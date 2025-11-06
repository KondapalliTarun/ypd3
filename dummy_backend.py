
import asyncio
import websockets
import json
import random
print("Script starting...")

async def handler(websocket, path):
    print(f"Client connected from {websocket.remote_address}")
    try:
        while True:
            # Simulate receiving frames from the client
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Received asanaNumber: {data.get('asanaNumber')}")

            # Simulate pose detection logic
            detection_result = {
                "data": random.randint(0, 3),
                "confidence": round(random.uniform(0.8, 1.0), 2)
            }
            await websocket.send(json.dumps(detection_result))
            await asyncio.sleep(1) # Simulate processing time
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected from {websocket.remote_address}")

async def main():
    print("Starting WebSocket server...")
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    print("Running main function...")
    asyncio.run(main())
