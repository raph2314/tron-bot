import asyncio
import websockets
import json

websocket_url = 'ws://35.183.103.104:8080/connect_dev'

sample_request = {
    'type':'REGISTRATION',
    'message':'',
    'authenticationKey':'<YOUR KEY>',
    'team_id':'<YOUR TEAM ID>'
    }

async def hello():
    async with websockets.connect(websocket_url) as websocket:
        message = input(json.dumps(sample_request))
        print(sample_request)

        await websocket.send(message)
        print(f"> {message}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())