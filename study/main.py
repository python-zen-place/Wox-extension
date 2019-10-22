from config import config
import os
import requests
from wox import Wox


class Study(Wox):
    def query(self, query):
        data = {
            'username': config['username'],
            'password': config['password']
        }
        if query == 'config':
            return [{
                'Title': 'study',
                'SubTitle': 'click here to config',
                'IcoPath': 'image/icon.png',
                'JsonRPCAction': {
                    'method': 'detail',
                    'dontHideAfterAction': True
                }
            }]
        elif query == 'today' or 'tomorrow':
            res = requests.post(config['url'] + query, data).json()['data']
            return [{
                'Title': info['course'] + ' ' + info['teacher'],
                'SubTitle': info['time'] + ' ' + info['classroom'],
                'IcoPath': 'image/icon.png'
            } for info in res.values()]
        else:
            return []

    def detail(self):
        os.system('explorer {}'.format(os.path.abspath('config/__init__.py')))


if __name__ == '__main__':
    Study()
