import os
import re
from wox import Wox, WoxAPI
from dns import dns
from multiprocessing import Pool
from ping import ping


def run_ping(server):
    data = ping(server)
    if 'ms' not in data:
        return {
            'Title': server,
            'SubTitle': '超时',
            'IcoPath': 'image/icon.png'
        }
    else:
        time = data.split('=')[-1]
        return {
            'Title': server,
            'SubTitle': time.strip(),
            'IcoPath': 'image/icon.png'
        }


def list_factory(dns, JsonRPCActionMethod=None):
    results = [{
        'Title': 'DNS',
        'SubTitle': server,
        'IcoPath': 'image/icon.png',
    } for server in dns]
    if JsonRPCActionMethod:
        for result in results:
            result['JsonRPCAction'] = {
                'method': JsonRPCActionMethod,
                'parameters': [result['SubTitle']],
                'dontHideAfterAction': True
            }
    return results


class DNS(Wox):
    def query(self, query):
        if query == 'list':
            return list_factory(dns, 'test')
        elif query == 'all':
            p = Pool(os.cpu_count())
            tasks = [p.apply_async(run_ping, args=(server,)) for server in dns]
            p.close()
            p.join()
            return sorted([res.get() for res in tasks],
                          key=lambda x: int(x['SubTitle'][:-2]) if x['SubTitle'] != '超时' else 10000)
        elif query.startswith('add'):
            ip = re.search('(\d{1,3}\.){3}\d{1,3}#', query)
            if ip:
                ip = ip.string.split()[1][:-1]
                if ip not in dns:
                    dns.append(ip)
                    data = ''.join(['\'{}\','.format(server) for server in dns])
                    with open('dns/__init__.py', 'w') as f:
                        f.write('dns = [{}]'.format(data))
            return list_factory(dns)
        elif query.startswith('remove'):
            ip = re.search('(\d{1,3}\.){3}\d{1,3}#', query)
            if ip:
                ip = ip.string.split()[1][:-1]
                if ip in dns:
                    data = ''.join(['\'{}\','.format(server) for server in dns if server != ip])
                    with open('dns/__init__.py', 'w') as f:
                        f.write('dns = [{}]'.format(data))
            return list_factory(dns, 'remove')
        elif re.match('(\d{1,3}\.){3}\d{1,3}#', query):
            return [ping(query)]

    def test(self, server):
        WoxAPI.change_query('dns ' + server + '#')

    def remove(self, server):
        WoxAPI.change_query('dns remove ' + server + '#')


if __name__ == '__main__':
    DNS()
