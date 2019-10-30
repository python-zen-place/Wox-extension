from config import config
import os
import requests
from wox import Wox

def run(command, package):
    with os.popen('pip {command} {package}'.format(command, package)) as res:
        data = res.split('\n')
        return [{
            'Title': 'ping',
            'SubTitle': statement,
            'IcoPath': 'image/icon.png'
        } for statement in data]


class WoxPip(Wox):
    def query(self, query):
        if query.endswith('#') and any(['install', 'remove', 'list']) in query:
            pip, command, package = query.split()
            return run(command, package)


if __name__ == '__main__':
    WoxPip()
