# coding=utf-8
from Config import config
from Unit import Parse
from Unit import Save


def run():
    item = {}
    # 把分类信息以列表形式返回,并且迭代
    for tag, num in config.tags_1.items():
        # item['tags'] = tag
        # print(item['tag'])
        # 分类列表页
        list_url = config.list_url.format(num)
        for albums_id in Parse.list_parse(list_url):
            item['albums_id'] = albums_id
            for Item in Parse.detail_parse(albums_id):
                items = dict(item, **Item)
                Save.save(items)


if __name__ == '__main__':
    run()
