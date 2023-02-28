

import requests
from requests.auth import HTTPBasicAuth
import json


def get_acess_token():
    BASE_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    consumer_key ='dWE70GWgmB8QKftsGVUtrdJkgAV8FS0z'
    consumer_secret = '4DFvA3mEChTcAsZF'
    response = requests.request("GET", BASE_URL, auth=HTTPBasicAuth(consumer_key , consumer_secret))

    access_token = json.loads(response.text)
    # print(response.text.encode('utf8'))
    print("acess" , access_token['access_token'])

    return access_token



