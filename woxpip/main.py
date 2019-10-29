from config import config
import os
import requests
from wox import Wox


class WoxPip(Wox):
    def query(self, query):
        if  query.endswith('#') and 'install' in query:
            with os.popen('pip install {}'.format()):
                pass


if __name__ == '__main__':
    WoxPip()
