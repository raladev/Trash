import websockets
import asyncio
import socket
import time
import base64
import zlib

import json
import hmac

from utils import load_config
from hashlib import sha256



#it works!
class OkexWsSubscriber:

    @property
    def LOGIN(self):
         try:
            config = load_config('../accounts.yml')
            timestamp = str(int(time.time()))
            api_key = config['Okex']['apikey']
            passphrase = config['Okex']['passphrase']
            secret_key = config['Okex']['secretkey']

            message = timestamp + 'GET' + '/users/self/verify'
            sign = base64.b64encode(hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'),
                                             digestmod='sha256').digest()).decode('utf-8')
            login_message = {"op": "login", "args": [api_key, passphrase, timestamp, sign]}
            return json.dumps(login_message)
         except Exception as e:
             print(e)


    def __init__(self, message_handler=None, connection_url='wss://real.okex.com:8443/ws/v3', loop=asyncio.get_event_loop()):
        self._message_handler = message_handler
        self.ws = None
        self._url = connection_url
        self._loop = loop
        self._listen_future = None

    async def listen(self):
        while True:
            try:
                print(await self.ws.recv())
            except websockets.ConnectionClosedError as e:
                print('ConnectionClosedError Exception in listen: {}'.format(e))
                await asyncio.sleep(2)
            except Exception as e:
                print('Unexpected Exception in listen: {}'.format(e))
                await asyncio.sleep(2)

    async def send(self, msg='hell-send'):
            try:
                await self.ws.send(msg)
                return True
            except websockets.ConnectionClosedError as e:
                print('ConnectionClosedError Exception in send: {}'.format(e))
                return False
            except Exception as e:
                print('Unexpected Exception in send: {}'.format(e))
                return False

    async def connect(self):
       while True:
        try:
            self.ws = await websockets.connect(self._url)
            print('connected')
            await self.send(msg=self.LOGIN)
            msg = await self.ws.recv()
            print(self.encode_message(msg))
            break
        except TimeoutError as e:
            print('Cant connect, need more time: {}'.format(e))
            await asyncio.sleep(3)
        except socket.gaierror as e:
            print('Cant connect, need more time: gai - {}'.format(e))
            await asyncio.sleep(3)

    def set_listener(self):
        self._reconnect_future = asyncio.ensure_future(self.reconnect_manager(), loop=self._loop)
        self._listen_future = asyncio.ensure_future(self.listen(), loop=self._loop)

    def _ping(self):
        pass

    def encode_message(self, data):
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated


