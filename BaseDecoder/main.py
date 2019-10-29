from wox import Wox
from base64 import b64decode
from binascii import Error


class BaseDecoder(Wox):
    def query(self, query):
        if not query:
            return []
        try:
            data = b64decode(query).decode('utf-8')
            result = [{
                'Title': 'BaseDecoder',
                'SubTitle': data,
                'IcoPath': 'image/icon.png'
            }]
        except Error as e:
            result = [{
                'Title': 'BaseDecoder',
                'SubTitle': '非法Base64串',
                'IcoPath': 'image/icon.png'
            }]
        return result


if __name__ == '__main__':
    BaseDecoder()
