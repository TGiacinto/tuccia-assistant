import requests
import json


def perform_request(method, url, headers=None, params=None, data=None):
    if method.lower() == "get":
        response = requests.get(url, headers=headers, params=params)
    elif method.lower() == "post":
        response = requests.post(url, headers=headers, params=params, data=json.dumps(data))
    elif method.lower() == "put":
        response = requests.put(url, headers=headers, params=params, data=json.dumps(data))
    elif method.lower() == "delete":
        response = requests.delete(url, headers=headers, params=params)
    else:
        print("Invalid method")
        return

    return response
