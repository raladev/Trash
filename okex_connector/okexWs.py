import websockets
import asyncio
import socket
import time
import base64
import zlib
from okex_connector.okexMessages import Msg
import json
import hmac

from utils import subsDict
from hashlib import sha256



#it works!
class OkexWsSubscriber:
    def __init__(self, message_handler=None, connection_url='wss://real.okex.com:8443/ws/v3', loop=asyncio.get_event_loop()):
        self._message_handler = message_handler
        self.ws = None
        self._url = connection_url
        self._loop = loop
        self._listen_future = None
        self.subscriptions = subsDict()

    def subscribe(self, only_one_channel, sub_handler=None):
        try:
            self.subscriptions[only_one_channel] = asyncio.ensure_future(self.async_subscribe(only_one_channel, sub_handler), loop=self._loop)
            return self.subscriptions[only_one_channel]
        except Exception as e:
            print('Unexpected Exception in subscribe: {}'.format(e))
            return False

    def unsubscribe(self, only_one_channel):
        try:
            self.subscriptions.get(only_one_channel).cancel()
            self.subscriptions.pop(only_one_channel)
            print("Successful unsubscription for {}", only_one_channel)
        except Exception as e:
            print('Unexpected Exception in unsubscribe: {}'.format(e))
            return False


    async def async_subscribe(self, channel, sub_handler=None):
        try:
            sub_message = json.dumps({"op": "subscribe", "args": [channel]})
            # TODO: add error message handling
            await self.send(msg=sub_message)
            while True:
                if sub_handler is None:
                    print(self.encode_message(await self.ws.recv()))
                else:
                    sub_handler(self.encode_message(await self.ws.recv()))
        except websockets.ConnectionClosedError as e:
            print('ConnectionClosedError Exception in listen: {}'.format(e))
            await asyncio.sleep(2)
        except asyncio.CancelledError:
            print("{} subscription cancelled", channel)
        except Exception as e:
            print('Unexpected Exception in listen: {}'.format(e))
            await asyncio.sleep(2)

    async def connect(self, init_msg=None):
        while True:
            try:
                self.ws = await websockets.connect(self._url)
                print('connected')

                if init_msg is not None:
                    await self.send(msg=init_msg)
                    # TODO: add error message handling
                    msg = await self.ws.recv()
                    print(self.encode_message(msg))

                break
            except TimeoutError as e:
                print('Cant connect, need more time: {}'.format(e))
                await asyncio.sleep(3)
            except socket.gaierror as e:
                print('Cant connect, need more time: gai - {}'.format(e))
                await asyncio.sleep(3)

    def _ping(self):
        pass

    async def send(self, msg='ping'):
        try:
            await self.ws.send(msg)
            return True
        except websockets.ConnectionClosedError as e:
            print('ConnectionClosedError Exception in send: {}'.format(e))
            return False
        except Exception as e:
            print('Unexpected Exception in send: {}'.format(e))
            return False

    async def recv(self):
        try:
            return self.encode_message(await self.ws.recv())
        except websockets.ConnectionClosedError as e:
            print('ConnectionClosedError Exception in send: {}'.format(e))
            return False
        except Exception as e:
            print('Unexpected Exception in send: {}'.format(e))
            return False

    def encode_message(self, data):
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated


