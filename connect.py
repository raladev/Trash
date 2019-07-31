import websockets
import asyncio
import socket
import time

#reconnect in alone function
async def test():
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
                          #  ws.
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




# 2 tasks
# Reconnect works automatically for short time, but ws.send sends all unsended messages;
async def test2_writer(ws):
    while True:
        try:
            while True:
                await ws.send('hell')
                await asyncio.sleep(1)
        except:
            print('im here')
            await asyncio.sleep(2)

async def test2_listener(ws):
    while True:
        try:
            while True:
                print(await ws.recv())
        except:
            await asyncio.sleep(2)


async def test2_task_manager():
    ws = await websockets.connect('ws://echo.websocket.org/')
    task1 = asyncio.create_task(test2_listener(ws))
    task2 = asyncio.create_task(test2_writer(ws))
    await asyncio.gather(task1, task2)






# Need to send new ws to writer and listener
async def test3_connection_manager(ws):
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
                ws = await websockets.connect('ws://echo.websocket.org/')
                #await ws.send('hell')
                #return ws
            except socket.gaierror:
                print('its , here we go again')
                await asyncio.sleep(2)

async def test3_writer(ws):
    while True:
        try:
            while True:
                await ws.send('hell')
                await asyncio.sleep(1)
        except:
            print('im here')
            await asyncio.sleep(1)
            ws = test3_connection_manager(ws)


async def test3_listener(ws):
    while True:
        try:
            while True:
                print(await ws.recv())
        except:
            await asyncio.sleep(2)


async def test3_task_manager():
    ws = await websockets.connect('ws://echo.websocket.org/')
    task1 = asyncio.create_task(test3_connection_manager(ws))
    task2 = asyncio.create_task(test3_listener(ws))
    task3 = asyncio.create_task(test3_writer(ws))
    await asyncio.gather(task1, task2, task3)


if __name__ == "__main__":
    # for test()
    # asyncio.get_event_loop().run_until_complete(test())

    # for test2()
    # asyncio.run(test2_task_manager())

    # for test3()
    asyncio.run(test3_task_manager())

