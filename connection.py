import asyncio
import websockets
import json

websocket_url = 'ws://35.183.103.104:8080/connect_dev'

team_id = '9'
team_key = '0fbe37d761047869af1891a0cea9cfb398f9b5cc'

team_id_dev = '29'
team_key_dev = 'f633fe93bf92864d22b1cd1d53452466ff0ab7b7'

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