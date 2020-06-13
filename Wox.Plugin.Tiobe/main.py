import requests
from wox import Wox
from lxml import etree

class Tiobe(Wox):
    def query(self, query):
        html = etree.HTML(requests.get('https://www.tiobe.com/tiobe-index/').text)
        table_content = html.xpath('//*[@id="top20"]/tbody/tr/*/text()')
        ranking_list = [x for i, x in enumerate(table_content) if i % 5 == 2]
       	return [{
       		'Title': f'{i+1}',
       		'SubTitle': f'{language}',
       		'IcoPath': 'image/icon.ico'
       	} for i, language in enumerate(ranking_list)]

if __name__ == '__main__':
    Tiobe()
