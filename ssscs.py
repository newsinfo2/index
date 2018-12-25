# coding=utf-8
import re
import time, threading
from time import ctime, sleep
import requests, json
from lxml import etree
import datetime
import time

url = 'http://rp.hpplay.cn/test'
cd = 0
hd = 0



def _test(url, cd, hd):
    for i in range(100000):
        res = requests.get(url)

        if res.status_code == 200:
            cd = cd + 1
        else:
            hd += 1

        print("成功次数为{},失败次数为{}".format(cd, hd))


if __name__ == '__main__':
    cs=ctime()
    _test(url, cd, hd)
    print("开始时间为 %s" % cs)
    print("结束时间为%s" % ctime())