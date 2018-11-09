import asyncio
import websockets
import json

websocket_url = 'ws://35.183.103.104:8080/connect_dev'

team_id = '<YOUR TEAM ID>'
team_key = '<YOUR KEY>'

sample_request = {
    'type':'REGISTRATION',
    'message':'',
    'authenticationKey':team_key,
    'team_id':team_id
    }

sample_move = {
    'type':'MOVE',
    'message':'UP',
    'authenticationKey':'<YOUR KEY>',
    'team_id':'<YOUR TEAM ID>'
    }

async def hello():
    async with websockets.connect(websocket_url) as websocket:
        message = json.dumps(sample_request)

        await websocket.send(message)

        answer = await websocket.recv()
        
        print(f"< FIRST_ANSWER :{answer}")

asyncio.get_event_loop().run_until_complete(hello())