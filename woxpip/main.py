import os
from wox import Wox
from OperationError import OperationError


def run(command, package):
    if 'ERROR' in res:
        raise OperationError
    if command == 'list':
        with os.popen('pip list') as res:
            data = res.split('\n')
            return [{
                'Title': 'ping',
                'SubTitle': statement,
                'IcoPath': 'image/icon.png'
            } for statement in data]
    elif command == 'uninstall':
        res = os.popen('pip show {}'.format(package))
        requires = res.split('Requires: ')[1].split('\n')[0].split(',')
        return [{
            'Title': 'ping',
            'SubTitle': '',
            'IcoPath': 'image/icon.png',
            'JsonRPCAction': {
                'method': '',
                'parameters': '',
                'dontHideAfterAction': True
            }
        }]

        class WoxPip(Wox):
            def query(self, query):
                command = list(filter(lambda x: x in query, ['install', 'remove', 'list']))
                assert len(command) == 1, "Command ERROR"
                command = command[0]
                pip, command, package = query.split()
                return run(command, package)

        if __name__ == '__main__':
            WoxPip()
