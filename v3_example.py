#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Roiy Zysman"
__version__ = "0.1.0"
__license__ = "MIT"

import os
import requests
from time import time
import urllib.parse
import hashlib
import hmac
import json
import time
import hashlib
import uuid


def bit_post():
        secret = 'YOUR BITTREX SECRET CODE'
        api_key= 'YOUR BITTREX API KEY'

        # Setting up an order to:
        # Sell 0.001 Bitcoin
        # with a limit of $10,000 usd per bitcoin 
        # and keep the order till cancelled 
        content = {"marketSymbol": "BTC-USD",
                   "direction": "SELL",
                   "type": "LIMIT",
                   "limit": "10000",
                   "quantity": "0.001",
                   "timeInForce": "GOOD_TIL_CANCELLED"
                   }


        payload = bytes(json.dumps(content), 'utf-8')
        timestamp = str(round(time.time()*1000))
        contentHash = hashlib.sha512(payload).hexdigest()
        method = 'POST'
        uri = 'https://api.bittrex.com/v3/orders'

        array = [timestamp, uri, method, contentHash]
        print (array)
        s = ''
        preSign = s.join(str(v) for v in array)
        signature = hmac.new(secret.encode(), preSign.encode(),
                        hashlib.sha512).hexdigest()

        header = {
        'Accept': 'application/json',
        'Api-Key': api_key,
        'Api-Timestamp': timestamp,
        'Api-Content-Hash': contentHash,
        'Api-Signature': signature,
        'Content-Type': 'application/json'
        }

        
        data = requests.post(uri, data=payload, headers=header, timeout=10).json()
        print(data)

        # Returned data looks something like this
        # {'id': '111111-1111-1111-1111-1111112d1', 'marketSymbol': 'BTC-USD', 'direction': 'SELL', 'type': 'LIMIT', 'quantity': '0.001', 'limit': '10000', 'timeInForce': 'GOOD_TIL_CANCELLED',
        # 'fillQuantity': '0.00000000', 'commission': '0.00000000', 'proceeds': '0.00000000', 'status': 'OPEN', 'createdAt': '2020-06-26T05:35:33.89Z', 'updatedAt': '2020-06-26T05:35:33.89Z'}



def main():
    """ Main entry point of the app """
    bit_post()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
