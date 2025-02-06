import requests
import json

def checker(token: str, imei: str = '123456789123456'):
    
    url = 'https://api.imeicheck.net/v1/checks'

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    body =  json.dumps({
        "deviceId": imei,
        "serviceId": 12
    })

    # Execute request
    response = requests.post(url, headers=headers, data=body)
    return response


if __name__ == "__main__":
    checker(input())