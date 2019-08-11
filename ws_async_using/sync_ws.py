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
                print('connection established')
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
            return True
        except websockets.ConnectionClosedError as e:
            print('ConnectionClosedError Exception in send: {}'.format(e))
            await self.async_connect()
        except Exception as e:
            print('Unexpected Exception in send: {}'.format(e))
            await self.async_connect()

    def read(self):
        return self._loop.run_until_complete(self.async_read())

    async def async_read(self):
        try:
            return await self.ws.recv()
        except websockets.ConnectionClosedError as e:
            print('ConnectionClosedError Exception in send: {}'.format(e))
            await self.async_connect()
        except Exception as e:
            print('Unexpected Exception in send: {}'.format(e))
            await self.async_connect()

    def send_and_get_answer(self, msg='do something'):
        return self._loop.run_until_complete(self.async_send_and_get_answer(msg))

    async def async_send_and_get_answer(self, msg='do something'):
        await self.async_send(msg)
        answer = None
        #read until we get correct message from the queue
        while answer != msg:
            answer = await self.async_read()
        return answer

    def ping(self):
        return self._loop.run_until_complete(self._ping())

    async def _ping(self):
        pong_waiter = await self.ws.ping()
        answer = await pong_waiter
        print(await pong_waiter)
        return answer

if __name__ == "__main__":
        ws = SyncWsConnection()
        ws.connect()
        print(ws.send_and_get_answer('gogen solntsev'))
        if ws.send('message without answer'):
            print('msg without answer sended')
        if ws.send('second message without answer'):
            print('second msg without answer sended')
        # read first msg from queue
        print(ws.read() + ' readed')
        # send msg and read from queue until get correct answer (second msg without answer will be read, skipped and lost)
        print(ws.send_and_get_answer('b  bs'))


