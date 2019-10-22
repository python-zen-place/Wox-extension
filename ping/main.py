import os
from wox import Wox


class Ping(Wox):
    def query(self, query):
        if not query:
            return []
        if not query.endswith('\n'):
            return []
        with os.popen('ping {} -4'.format(query)) as res:
            data = [s.strip() for s in res.read().split('\n') if s != '']
        results = [{
            'Title': 'ping',
            'SubTitle': statement,
            'IcoPath': 'image/icon.png'
        } for statement in data]
        return results


if __name__ == '__main__':
    Ping()
