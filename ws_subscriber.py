import websockets
import asyncio
import socket
import time

#it works!
class WsSubscriber:

    def __init__(self, message_handler=None, connection_url='ws://echo.websocket.org/', loop=asyncio.get_event_loop()):
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
                await asyncio.sleep(2)
                return True
            except websockets.ConnectionClosedError as e:
                print('ConnectionClosedError Exception in send: {}'.format(e))
                return False
            except Exception as e:
                print('Unexpected Exception in send: {}'.format(e))
                return False

    async def inf_send(self, msg='hell-send'):
        while True:
            try:
                await self.ws.send(msg)
                await asyncio.sleep(2)
            except websockets.ConnectionClosedError as e:
                print('ConnectionClosedError Exception in send: {}'.format(e))
                await asyncio.sleep(2)
            except Exception as e:
                print('Unexpected Exception in send: {}'.format(e))
                await asyncio.sleep(2)

    async def reconnect_manager(self):
        while True:
            try:
                pong = await self.ws.ping()
                await asyncio.wait_for(pong, timeout=2)
                print('Ping OK')
                await asyncio.sleep(2)
            except asyncio.TimeoutError:
                print('No pong')
                await asyncio.sleep(2)
            except:
                print('Connection troubles: {}')
                self.ws.close_connection()
                await self.connect()

    async def connect(self):
       while True:
        try:
            self.ws = await websockets.connect(self._url)
            #some init messages
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

    def set_listener_with_inf_send(self):
        self._reconnect_future = asyncio.ensure_future(self.reconnect_manager(), loop=self._loop)
        self._listen_future = asyncio.ensure_future(self.listen(), loop=self._loop)
        self._listen_future = asyncio.ensure_future(self.inf_send(), loop=self._loop)

    def _ping(self):
        pass


#async def main(loop):
#    ws = WsSubscriber(loop=loop)
#    await ws.connect()
#    ws.set_listener_with_inf_send()
#    await asyncio.sleep(10)


#works only 10 seconds
#if __name__ == "__main__":
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(main(loop))


async def second_main(loop):
    ws = WsSubscriber(loop=loop)
    await ws.connect()
    ws.set_listener()
    await ws.send('heeyea')
    await ws.send('heeyea2')
    await ws.send('heeyea3')
    await ws.send('heeyea4')
    await ws.send('heeyea5')
    print('End of main')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    #waits end of the second_main()
    loop.run_until_complete(second_main(loop))
    print('Loop stopped')
    loop.run_until_complete(second_main(loop))
    print('Loop stopped again')

