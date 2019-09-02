import websockets
import asyncio
import socket
import time


async def standalone_reconnect():
    while True:
        try:
            async with websockets.connect('ws://echo.websocket.org/') as ws:
                while True:
                    try:
                        await ws.send('hello')
                        print(await ws.recv())
                        await asyncio.sleep(1)
                    except websockets.ConnectionClosedError:
                        try:
                            pong = await ws.ping()
                            await asyncio.wait_for(pong, timeout=2)
                            print('Ping OK')
                            continue
                        except:
                            await asyncio.sleep(3)
                            print('No pong')
                            break  # inner loop
        except socket.gaierror:
            print('its , here we go again')
            time.sleep(1)
            continue








async def no_reconnect_writer(ws):
    while True:
        try:
            while True:
                await ws.send('hell')
                await asyncio.sleep(1)
        except:
            print('im here')
            await asyncio.sleep(2)

async def no_reconnect_listener(ws):
    while True:
        try:
            while True:
                print(await ws.recv())
        except:
            await asyncio.sleep(2)

async def no_recconect_task_manager():
    ws = await websockets.connect('ws://echo.websocket.org/')
    task1 = asyncio.create_task(no_reconnect_listener(ws))
    task2 = asyncio.create_task(no_reconnect_writer(ws))
    await asyncio.gather(task1, task2)






# Need to send new ws to writer and listener
async def connection_manager(ws):
    while True:
        try:
            pong = await ws.ping()
            await asyncio.wait_for(pong, timeout=2)
            print('Ping OK')
            await asyncio.sleep(2)
        except asyncio.TimeoutError:
            print('No pong')
            await asyncio.sleep(2)
        except:
            print('No connection?')
            try:
                print('hell')
                ws = websockets.connect('ws://echo.websocket.org/')
                #await ws.send('hell')
                #return ws
            except socket.gaierror:
                print('its , here we go again')
                await asyncio.sleep(2)

async def reconnect_writer(ws):
    while True:
        try:
            while True:
                await ws.send('hell')
                await asyncio.sleep(1)
        except:
            print('im here')
            await asyncio.sleep(1)
            await connection_manager(ws)


async def reconnect_listener(ws):
    while True:
        try:
            while True:
                print(await ws.recv())
        except:
            await asyncio.sleep(2)


async def reconnect_task_manager():
    ws = await websockets.connect('ws://echo.websocket.org/')
 #   task1 = asyncio.create_task(connection_manager(ws))
    task2 = asyncio.create_task(reconnect_listener(ws))
    task3 = asyncio.create_task(reconnect_writer(ws))
    await asyncio.gather(task2, task3)







#it works!
class TheStongestSocketInTheWorld:

    def __init__(self, message_handler=None, connection_url='ws://echo.websocket.org/'):
        self._message_handler = message_handler
        self.ws = None
        self._url = connection_url

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
            break
        except TimeoutError as e:
            print('Cant connect, need more time: {}'.format(e))
            await asyncio.sleep(3)
        except socket.gaierror as e:
            print('Cant connect, need more time: gai - {}'.format(e))
            await asyncio.sleep(3)

    def _ping(self):
        pass

async def test4_task_manager():
    ws = TheStongestSocketInTheWorld(None)
    await ws.connect()
    task1 = asyncio.create_task(ws.reconnect_manager())
    task2 = asyncio.create_task(ws.listen())
    task3 = asyncio.create_task(ws.send())
    ttl = await asyncio.gather(task1, task2, task3)
























