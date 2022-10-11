import time
import base64
import json
import hmac
import requests
import hashlib


# Example for create deposit addresses in python
api_secret = ''
api_passphrase = ''
api_key = ''
url = 'https://api.kucoin.com/api/v1/deposit-addresses'
now = int(time.time() * 1000)
data = {"currency": "BTC"}
data_json = json.dumps(data)
str_to_sign = str(now) + 'POST' + '/api/v1/deposit-addresses' + data_json
signature = base64.b64encode(
    hmac.new(
        api_secret.encode('utf-8'),
        str_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
)
passphrase = base64.b64encode(
    hmac.new(
        api_secret.encode('utf-8'),
        api_passphrase.encode('utf-8'),
        hashlib.sha256
    ).digest()
)
headers = {
    "KC-API-SIGN": signature,
    "KC-API-TIMESTAMP": str(now),
    "KC-API-KEY": api_key,
    "KC-API-PASSPHRASE": passphrase,
    "KC-API-KEY-VERSION": '2',
    "Content-Type": "application/json"
}
response = requests.request('post', url, headers=headers, data=data_json)
print(response.status_code)
print(response.json())
