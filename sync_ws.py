import websockets
import asyncio
import socket
import time


#it works!
class SyncWsConnection:

    def __init__(self, connection_url='ws://echo.websocket.org/', loop=asyncio.get_event_loop()):
        self.ws = None
        self._url = connection_url
        self._loop = loop

    def connect(self):
        return self._loop.run_until_complete(self.async_connect())

    async def async_connect(self):
        while True:
            try:
                self.ws = await websockets.connect(self._url)
                #some init messages
                return True
            except TimeoutError as e:
                print('Cant connect, need more time: {}'.format(e))
                time.sleep(2)
            except socket.gaierror as e:
                print('Cant connect, need more time: gai - {}'.format(e))
                time.sleep(2)

    def send(self, msg):
        return self._loop.run_until_complete(self.async_send(msg))

    async def async_send(self, msg='hell-send'):
        try:
            await self.ws.send(msg)
            await asyncio.sleep(2)
            return True
        except websockets.ConnectionClosedError as e:
            print('ConnectionClosedError Exception in send: {}'.format(e))
            await self.async_connect()
        except Exception as e:
            print('Unexpected Exception in send: {}'.format(e))
            await self.async_connect()

    def ping(self):
        return self._loop.run_until_complete(self._ping())

    async def _ping(self):
        pong_waiter = await self.ws.ping()
        print(await pong_waiter)
        return True

