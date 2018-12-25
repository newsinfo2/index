# coding=utf-8
import re
import requests, json
from lxml import etree
from Config import config
from bs4 import BeautifulSoup
import datetime
import time
from Unit import Save

headers ={
    "Connection":"keep-alive",
    "Referer":"http://movie.youku.com/?spm=a2hww.11359951.m_26658.5~1~3~8!2~A",
    "User-Agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/67.0.3396.99 Safari/537.36"

}
headerss ={
    "Connection":"keep-alive",
    "Referer":"http://movie.youku.com/?spm=a2hww.11359951.m_26658.5~1~3~8!2~A",
    "User-Agent":"Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML,like Gecko)Chrome/67.0.3396.99 Safari/537.36",
    'cookie':'P_F=1;P_T=1532172710;u_l_v_t=114;__ysuid=1524358525963lAB;cna=6M0wE0SCwmsCAbfpWd5xQzws;juid=01chi232j21quv;seid=01ciu2ogtg268f;referhost=https%3A%2F%2Fwww.baidu.com;yseid=1532165374951DpO6Ji;yseidcount=3;ycid=0;__ayft=1532165376496;__aysid=15321653765060lu;__arycid=cms-00-1519-27244-0;__ayscnt=1;__arcms=cms-00-1519-27244-0;P_ck_ctl=0905A3CD2F354DC35186205CA2D45136;rpvid=1532165391076cDnQfR-1532165428053;__utmarea=;__arpvid=1532165435355LrYmsO-1532165435389;__aypstp=4;__ayspstp=4;_m_h5_tk=8c61d56b38a5b070085c457a9d19a886_1532170479158;_m_h5_tk_enc=28e792abf84d4eb9b2b90a77aea626c4;seidtimeout=1532167239070;ypvid=15321654401120oDCKw;ysestep=3;yseidtimeout=1532172640116;ystep=5;_uab_collina=153216544385081928794871;_umdata=85957DF9A4B3B3E8080A62D85409F1F6983F6F5BE479CB51ACC0F7D1B42CEE1C4CFF2FC675CDA4C2CD43AD3E795C914C16DE937286D7418910D4D5AB47C5BC36;isg=BD09zOpLOg4Wf54MHGvdKtuITJD3cjGq5GheZf-CMRTDNl1oxyqB_AvM5CrVtonk;__ayvstp=4;__aysvstp=4'
}


# 数据请求模块返回列表页内容
def _requests(url,times=0):
    try:
        res = requests.get(url, headers=headerss,timeout=30)
        res.encoding = 'utf-8'
        return res.content
    except:
        times += 1
        print('尝试第{}次请求'.format(times) if times <= 5 else '请求失败,停止请求')
        return _request(url, times) if times <= 5 else None
def _request(url, times=0):
    try:
        res = requests.get(url, headers=headerss,timeout=30)
        res.encoding = 'utf-8'
        return res.text
    except:
        times += 1
        print('尝试第{}次请求'.format(times) if times <= 5 else '请求失败,停止请求')
        return _request(url, times) if times <= 5 else None


# 解析最后一页页码,并生成url
def _list(url):
    urld = 'http://list.youku.com/category/video/c_94_d_1_s_1_p_1.html'
    response = _request(urld)
    # 如果返回的内容不是空的
    if response is not None:
        # 转换成HTML格式
        html = etree.HTML(response)
        # 解析最后一页页码
        # print(url)
        if html is not None:
            total_list = html.xpath("//ul[@class = 'yk-pages']/li/a/text()")
            # 如果返回数据长度不等于0，取最后一个就是最大页码，如果为0 表示只有1页
            total = int(total_list[-2]) if len(total_list) != 0 else 1
            # print(total_list)
            for i in range(total):
                tsgs = str(url).replace('http://list.youku.com/category/video/c_94_g_', '').replace(
                    '_d_1_s_1_p_{}.html', '')
                urls = 'http://list.youku.com/category/video/c_176_d_1_s_1_p_{}.html'
                yield urls.format(i+1)
        else:
            return []
    else:
        return []


# 解析列表页数据
def list_parse(url):
    for next_url in _list(url):
        print(next_url)
        response = _request(next_url)
        # print(response)
        if response is not None:
            html = etree.HTML(response)
            if html is not None:
                hrefs = html.xpath("//div[@class = 'yk-pack p-list']/div/a/@href")
                # print(hrefs)
                for href in hrefs:
                    # 返回的数据就是电视剧的链接，链接中包含电视剧id
                    albums_id = str(href).split("id_")[1].split(".")[0]
                    # print(href)
                    if 'javascript' not in albums_id:
                        yield albums_id


# 解析详情页,传入专辑id
def detail_parse(albums_id):
    item = {}
    albums_url = "http://v.youku.com/v_show/id_{}.html".format(albums_id)
    # print(albums_url)
    response = _request(albums_url)
    if response is not None:
        html = etree.HTML(response)
        list_u = html.xpath("//h2/a/@href")
        url_dd = ''.join(list_u)
        url_d = 'https:'+url_dd
        # print(url_d)
        resp = _request(url_d)
        if resp is not None:
            htm = etree.HTML(resp)
            list_r = htm.xpath("//ul[@class = 'nav-menu']/li[2]/a/@href")
            if len(list_r) > 0:
                url_h = "https://i.youku.com"+''.join(list_r)
                # print(url_h)
                res = _request(url_h)
                if res is not None:
                    xml = etree.HTML(res)
                    total_lis = xml.xpath("//ul[@class = 'yk-pages']/li/a/text()")
                    total = int(total_lis[-2]) if len(total_lis) != 0 else 1
                    # print(total)
                    list_str = ''.join(list_r)
                    # print(list_str)
                    albums_sd = str(list_str).replace('/i/', '').replace('/videos', '')
                    item['albums_id'] = albums_sd
                    # print(albums_sd)
                    list_urls = []
                    for i in range(total):
                        url_l = 'https://i.youku.com/i/{}/videos?page={}'
                        url_c = url_l.format(albums_sd,i+1)
                        list_urls.append(url_c)
                    url__li = []
                    # print(list_urls)
                    for i in list_urls:
                        responses = _request(i)
                        x_ml = etree.HTML(responses)
                        url_lis = x_ml.xpath("//div[@class = 'items']/div/div[@class ='v-link' ]/a/@href")
                        for o in url_lis:
                            url__li.append(o)
                    # print (len(url__li))
                    for i in url__li:
                        url = 'https:' + i
                        # print(url)
                        if Save.repeated_detect(url):
                            rees = _request(url)
                            xm_l = etree.HTML(rees)
                            if html is not None:
                                titles = xm_l.xpath("//span[@id='subtitle']/text()")
                                title = titles[0] if len(titles) != 0 else None
                                item['title'] = title
                                if title is not None:
                                    item["spider_type"] = 1

                                    # // 入库时间   值是这种格式                                    # item['title'] = title
                                    item["media_update_day"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                                    # 电影来源
                                    item["media_type"] = "youku"
                                    item["media_update_date"] = datetime.datetime.now().strftime("%Y%m%d%H%m%S")
                                    # 推荐
                                    # 推荐
                                    urs = xm_l.xpath("//ul[@class ='info-list']/li/a/@href")
                                    dds = xm_l.xpath("//ul[@class ='info-list']/li/a/text()")
                                    cd = []
                                    for i, d in zip(urs, dds):
                                        f = 'http:' + i
                                        cd.append(d)
                                        cd.append(f)

                                    href = xm_l.xpath("//div[@class = 'rows']/div/div[@class = 'title']/a/@href")
                                    tits = xm_l.xpath("//div[@class = 'rows']/div/div[@class = 'title']/a/@title")
                                    recommed = []
                                    for i, d in zip(href, tits):
                                        f = 'http:' + i
                                        recommed.append(d)
                                        recommed.append(f)
                                    if len(cd) > 1:

                                        item['recommend_video'] = cd
                                    else:

                                        item['recommend_video'] = recommed
                                    tgs = ['自拍']
                                    cl = xm_l.xpath("//span[@data-sn='tags']/a/text()")
                                    lr = tgs + cl
                                    item['tags'] = lr
                                    item['media_film_type'] = tgs
                                    item['remove_id'] = 'youku_zp'
                                    item['url'] = url
                                    media_d = url.split("id_")[1].split(".")[0]
                                    # 视频id
                                    item['media_id'] = media_d
                                    # 评论
                                    if item['media_id'] != '':
                                        comment_item = []
                                        try:
                                            comment_resd = requests.get(
                                                'https://p.comments.youku.com/ycp/comment/pc/commentList?jsoncallback=n_commentList&app=100-DDwODVkv&objectId={}&objectType=1&listType=0&currentPage=1&pageSize=30&sign=77c823267e3e514ce37168cddbe705e6&time=1545292740'.format(
                                                    media_d), headers=headers)
                                            try:
                                                comment_resd.encoding = 'utf-8'
                                                comment_res = comment_resd.text[16:-1]
                                                if comment_res is not None:
                                                    try:
                                                        comment_json = json.loads(comment_res)
                                                        # print(comment_json)
                                                        if comment_json is not None:
                                                            try:
                                                                comment_list = comment_json['data']['comment']
                                                                # print(comment_list)
                                                                for comment in comment_list:
                                                                    comment_item.append(comment['content'])
                                                                    # print(comment)
                                                                    comment_item.append(comment['user'])
                                                                item['comment'] = comment_item
                                                            except:
                                                                item['comment'] = []
                                                        else:
                                                            item['comment'] = []
                                                    except:
                                                        item['comment'] = []
                                                else:
                                                    item['comment'] = []
                                            except:
                                                item['comment'] = []
                                        except:
                                            item['comment'] = []
                                    else:
                                        item['comment'] = []
                                    yield item
            else:
                episodec = htm.xpath("//li[@class ='p-row p-renew' ]/text()")
                episodes = ''.join(episodec)
                try:
                    num = re.search('\d+', episodes).group()
                    # print(num)
                    ios = int(num)
                except:
                    ios = int(500)
                # 导演
                try:
                    item['albums_id'] = str(url_d).split('id_')[1].split('.')[0]
                except:
                    return
                cc = BeautifulSoup(resp, "lxml")
                sss = cc.select("div.p-base ul li")
                for i in sss:
                    sd = i.get_text()
                    if "主持人" in sd:
                        item['actors'] = sd.split("：")[1]

                for i in sss:
                    sd = i.get_text()
                    if "类型" in sd:
                        item['tags'] = sd.split("：")[1]
                    else:
                        item['tags'] = '自拍'
                # item['actors'] = res.xpath("//li[@class = 'p-performer']/a/text()")
                # 简介
                description_list = htm.xpath('//span[@class="text"]/text()')
                description = description_list[0] if len(description_list) != 0 else ''
                item['description'] = description
                # print(description)
                # 评分
                score_list = htm.xpath("//li[@class = 'p-score']/span/text()")
                score = score_list[0] if len(score_list) != 0 else ''
                item['score'] = score
                item['remove_id'] = 'youku_zp'
                # 剧集
                uu = []
                if ios > 5000:
                    ios = 500
                # print(ios)
                if ios > 30:
                    pages = int(ios / 30)
                    page = pages + 1
                    for i in range(page):
                        urlrs = "https://v.youku.com/page/playlist?&componentid=38011&videoCategoryId=97&isSimple=false&videoEncodeId={}&page={}".format(
                            albums_id, i + 1)
                        res = _requests(urlrs)
                        ress = etree.HTML(res)
                        dds = ress.xpath('//a/@href')
                        for dd in dds:
                            aa = str(dd).replace('\\"', "")
                            url = "http:" + ("".join(aa))
                            uu.append(url)
                else:
                    urlrs = "https://v.youku.com/page/playlist?&componentid=38011&videoCategoryId=97&isSimple=false&videoEncodeId={}&page=1".format(
                        albums_id)
                    res = _requests(urlrs)
                    ress = etree.HTML(res)
                    dds = ress.xpath('//a/@href')
                    for dd in dds:
                        aa = str(dd).replace('\\"', "")
                        url = "http:" + ("".join(aa))
                        uu.append(url)
                # print(uu)
                for url in uu:
                    # 去重判断
                    # print(urlw)
                    if Save.repeated_detect(url):
                        # url ="http:" + ("".join(url))
                        res = _request(url)
                        if res is not None:
                            Html = etree.HTML(res)
                            if Html is not None:
                                episodes = Html.xpath("//span[@id='subtitle']/text()")
                            else:
                                episodes = []
                            episode = (''.join(episodes)).strip() if len(episodes) != 0 else ''
                            item['url'] = url
                            # item['albums_id']=str(url).strip().split('s=')[-1]
                            # 集数
                            item['episode'] = episode
                            # print(episode)
                            # 视频id
                            medie = (str(url).split('id_'))[1].split('.html')[0] if len(
                                str(url).split('id_')) == 2 else ''
                            item['media_id'] = medie
                            item["spider_type"] = 1
                            # item['title'] = title
                            item["media_update_day"] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                            # 电影来源
                            item["media_type"] = "youku"
                            # // 入库时间   值是这种格式
                            item["media_update_date"] = datetime.datetime.now().strftime("%Y%m%d%H%m%S")
                            # 推荐
                            urs = Html.xpath("//ul[@class ='info-list']/li/a/@href")
                            dds = Html.xpath("//ul[@class ='info-list']/li/a/text()")
                            cd = []
                            for i, d in zip(urs, dds):
                                f = 'http:' + i
                                cd.append(d)
                                cd.append(f)

                            href = Html.xpath("//div[@class = 'rows']/div/div[@class = 'title']/a/@href")
                            tits = Html.xpath("//div[@class = 'rows']/div/div[@class = 'title']/a/@title")
                            recommed = []
                            for i, d in zip(href, tits):
                                f = 'http:' + i
                                recommed.append(d)
                                recommed.append(f)
                            if len(cd) > 1:

                                item['recommend_video'] = cd
                            else:

                                item['recommend_video'] = recommed
                            tgs = ['自拍']
                            item['media_film_type'] = tgs
                            # print(item['media_id'])
                            item['title'] = Html.xpath("//div[@class = 'tvinfo']/h2/a/text()")
                            # 评论
                            if item['media_id'] != '':
                                comment_item = []
                                try:
                                    comment_resd = requests.get(
                                        'https://p.comments.youku.com/ycp/comment/pc/commentList?jsoncallback=n_commentList&app=100-DDwODVkv&objectId={}&objectType=1&listType=0&currentPage=1&pageSize=30&sign=77c823267e3e514ce37168cddbe705e6&time=1545292740'.format(
                                            medie), headers=headers)
                                    try:
                                        comment_resd.encoding = 'utf-8'
                                        comment_res = comment_resd.text[16:-1]
                                        if comment_res is not None:
                                            try:
                                                comment_json = json.loads(comment_res)
                                                # print(comment_json)
                                                if comment_json is not None:
                                                    try:
                                                        comment_list = comment_json['data']['comment']
                                                        # print(comment_list)
                                                        for comment in comment_list:
                                                            comment_item.append(comment['content'])
                                                            # print(comment)
                                                            comment_item.append(comment['user'])
                                                        item['comment'] = comment_item
                                                    except:
                                                        item['comment'] = []
                                                else:
                                                    item['comment'] = []
                                            except:
                                                item['comment'] = []
                                        else:
                                            item['comment'] = []
                                    except:
                                        item['comment'] = []
                                except:
                                    item['comment'] = []
                            else:
                                item['comment'] = []
                            yield item
if __name__ == '__main__':
    albums_id = '639agzdh10yu2q2'
    detail_parse(albums_id)
