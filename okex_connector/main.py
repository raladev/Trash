from okex_connector.okexWs import OkexWsSubscriber
from okex_connector.okexMessages import Msg
import asyncio

async def main(loop):
    okexWs = OkexWsSubscriber(loop=loop)
    await okexWs.connect(init_msg=Msg.build_login_msg())
    okexWs.subscribe(Msg.Spot_Orderbook5_ETHUSD)
    await asyncio.sleep(3)
    okexWs.unsubscribe(Msg.Spot_Orderbook5_ETHUSD)
    await asyncio.sleep(3)
    print("And again")
    #Messages from previos subscription getted
    okexWs.subscribe(Msg.Spot_Orderbook5_ETHUSD)
    await asyncio.sleep(3)
    okexWs.unsubscribe(Msg.Spot_Orderbook5_ETHUSD)
    await asyncio.sleep(3)

#works only 10 seconds
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
