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


class Msg:
    @staticmethod
    def build_login_msg():
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

    Spot_Orderbook5_ETHUSD = ["spot/depth5:ETH-USDT"]
