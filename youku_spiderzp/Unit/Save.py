# coding=utf-8
import hashlib
from pymongo import MongoClient
from Config import config

conn = MongoClient(
   host='s-wz9defb14c342824.mongodb.rds.aliyuncs.com',port=3717

)
# conn = MongoClient(
#    host=config.host,port=config.port

# )
db_auth = conn.admin
db_auth.authenticate("root","LEBO!@#321")
db = conn[config.db]

client = db[config.collection]
Client = db[config.Collection]
connectTimeout=30000
connectionsPerHost=20
threadsAllowedToBlockForConnectionMultiplier=10
maxWaitTime=30000
autoConnectRetry=True
socketKeepAlive=True
#Socket超时时间
socketTimeout=30000
slaveOk=True
isAuth=True



def _Md5(string):
    hl = hashlib.md5()
    hl.update(string.encode(encoding='utf-8'))
    hash = hl.hexdigest()
    return hash[8:-8]


def save(item):
    sav = 'youku' + "_" + item["media_id"]
    item['_id'] = sav
    try:
        client.insert(item)
        print('Save success:{},{}'.format(item['title'], item['url']))
    except:
        print('Save failed:{},{}'.format(item['title'],item['url']))


# 去重检测
def repeated_detect(url):
    try:
        urd = [{"_id": _Md5(url),"spider_type":'youku_cysp'}]
        Client.insert(urd)
        return True
    except:
        return False


if __name__ == '__main__':
    save()
