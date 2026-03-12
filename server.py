import asyncio
import websockets
import json

sessions = {} # token -> [ws1, ws2]

async def handler(websocket, path):
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")
            token = data.get("token")
            
            if action == "host":
                if token not in sessions:
                    sessions[token] = [websocket]
                    await websocket.send(json.dumps({"status": "hosted", "token": token}))
                else:
                    await websocket.send(json.dumps({"status": "error", "msg": "Token in use"}))
                    
            elif action == "join":
                if token in sessions and len(sessions[token]) == 1:
                    sessions[token].append(websocket)
                    # Notify both that game is ready
                    for ws in sessions[token]:
                        await ws.send(json.dumps({"status": "ready"}))
                else:
                    await websocket.send(json.dumps({"status": "error", "msg": "Invalid token or full"}))
                    
            elif action == "state":
                if token in sessions:
                    # Relay state to the other peer
                    for ws in sessions[token]:
                        if ws != websocket:
                            await ws.send(json.dumps({"status": "state", "payload": data.get("payload")}))
                            
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Cleanup
        for token, clients in list(sessions.items()):
            if websocket in clients:
                clients.remove(websocket)
                for ws in clients:
                    try:
                        await ws.send(json.dumps({"status": "disconnected"}))
                    except: pass
                if not clients:
                    del sessions[token]

async def main():
    print("Signaling server running on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
