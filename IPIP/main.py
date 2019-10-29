import re
import requests
from wox import Wox


class IPIP(Wox):
    def query(self, query):
        if not query:
            return []
        ip = re.search(r'(\d{1,3}\.){3}\d{1,3}', query)
        if not ip:
            return []
        ip = ip.string
        URL = 'http://freeapi.ipip.net/{}'.format(ip)
        data = ' '.join(requests.get(URL).json())
        result = [{
            'Title': 'IPIP',
            'SubTitle': data,
            'IcoPath': 'image/icon.png'
        }]
        return result


if __name__ == '__main__':
    IPIP()