import os
import json
import requests
from wox import Wox, WoxAPI


class ShortURL(Wox):
    def query(self, query):
        API = 'https://api.uomg.com/api/long2dwz?dwzapi=tcn&url=https://'
        URL = f'{API}{query}'
        data = json.loads(requests.get(URL).text)
        if 'ae_url' in data.keys():
            shorten_url = data['ae_url']
        else:
            shorten_url = 'Vaild URL'
        result = [{
            'Title': 'ShortURL',
            'SubTitle': shorten_url,
            'IcoPath': 'image/icon.png',
            "JsonRPCAction":{
              "method": "copyResult",
              "parameters": [shorten_url],
              "dontHideAfterAction":False
            }
        }]
        return result
         
    def copyResult(self,shorten_url):
        os.popen(f"echo {shorten_url} | clip")

if __name__ == '__main__':
    ShortURL()
