# coding=utf-8
import re
import requests, json
from lxml import etree
from Config import config
from bs4 import BeautifulSoup

import datetime
import time
from Unit import Save
from bs4 import BeautifulSoup
import random
headerss = {
    "Connection": "keep-alive",
    "Referer": "http://movie.youku.com/?spm=a2hww.11359951.m_26658.5~1~3~8!2~A",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    'cookie':'P_F=1; P_T=1532172710; u_l_v_t=114; __ysuid=1524358525963lAB; cna=6M0wE0SCwmsCAbfpWd5xQzws; juid=01chi232j21quv; seid=01ciu2ogtg268f; referhost=https%3A%2F%2Fwww.baidu.com; yseid=1532165374951DpO6Ji; yseidcount=3; ycid=0; __ayft=1532165376496; __aysid=15321653765060lu; __arycid=cms-00-1519-27244-0; __ayscnt=1; __arcms=cms-00-1519-27244-0; P_ck_ctl=0905A3CD2F354DC35186205CA2D45136; rpvid=1532165391076cDnQfR-1532165428053; __utmarea=; __arpvid=1532165435355LrYmsO-1532165435389; __aypstp=4; __ayspstp=4; _m_h5_tk=8c61d56b38a5b070085c457a9d19a886_1532170479158; _m_h5_tk_enc=28e792abf84d4eb9b2b90a77aea626c4; seidtimeout=1532167239070; ypvid=15321654401120oDCKw; ysestep=3; yseidtimeout=1532172640116; ystep=5; _uab_collina=153216544385081928794871; _umdata=85957DF9A4B3B3E8080A62D85409F1F6983F6F5BE479CB51ACC0F7D1B42CEE1C4CFF2FC675CDA4C2CD43AD3E795C914C16DE937286D7418910D4D5AB47C5BC36; isg=BD09zOpLOg4Wf54MHGvdKtuITJD3cjGq5GheZf-CMRTDNl1oxyqB_AvM5CrVtonk; __ayvstp=4; __aysvstp=4'
}
# BeautifulSoup 获取
# url = 'https://v.youku.com/v_show/id_XMzc4NTQ5MDU5Mg==.html?spm=a2h1n.8251845.0.0'
# res = requests.get(url,headers=headerss)
# res.encoding = 'utf-8'
# ress = res.content
# html = etree.HTML(ress)
# cc = BeautifulSoup(ress, "lxml")
# sss = cc.select("div.p-base ul li")
# # print(sss)
# for i in sss:
#     sd = i.get_text()
#     if "类型" in sd:
#         cddd = sd.split("：")[1]
# xpath
url = 'http://v.youku.com/v_show/id_XMzk1OTI2Mzg4NA==.html?spm=a2h1n.8251846.0.0'
res = requests.get(url,headers=headerss)
res.encoding = 'utf-8'
ress = res.content
html = etree.HTML(ress)
hd = html.xpath("//h2/a/@href")
# cd = ''.join(hd)
# s = ['/i/UMTIwODUyMDM1Ng==/videos']

print (hd)