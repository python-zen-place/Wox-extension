import os
import uuid
from wox import Wox


class UUID(Wox):
    def query(self, query):
        data = str(uuid.uuid4())
        result = [{
            'Title': 'UUID',
            'SubTitle': data,
            'IcoPath': 'image/icon.png',
            "JsonRPCAction":{
              "method": "copyResult",
              "parameters":[data],
              "dontHideAfterAction":False
            }
        }]
        return result
    def copyResult(self,data):
        os.popen(f"echo {data} | clip")

if __name__ == '__main__':
    UUID()
