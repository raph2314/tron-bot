#!/usr/bin/env python3

# WS client example

import asyncio
import websockets
import json

message = {
        "type":"MOVE",  
        "message":"DOWN",
        "authenticationKey":"<YOUR KEY>",
        "team_id":"<YOUR TEAM ID>"
        }
json_msg = json.dumps(message)
loaded_msg = json.loads(json_msg)
async def hello():
    async with websockets.connect(
            'ws://35.183.103.104:8080/connect_dev') as websocket:
        name = input("What's your name? ")

        await websocket.send(loaded_msg)
        print(f"> {name}")

        greeting = await websocket.recv()
        

asyncio.get_event_loop().run_until_complete(hello())
