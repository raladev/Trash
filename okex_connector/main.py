from okex_connector.okexWs import OkexWsSubscriber
import asyncio

async def main(loop):
    ws = OkexWsSubscriber(loop=loop)
    await ws.connect()
    await asyncio.sleep(6)


#works only 10 seconds
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
