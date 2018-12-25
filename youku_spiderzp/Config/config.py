# coding=utf-8

# 列表页url
list_url = 'http://list.youku.com/category/video/c_94_g_{}_d_1_s_1_p_1.html'
# 播放页url
video_url = 'https://v.youku.com/v_show/{}.html'
# 播放基础
base_url = 'https://v.qq.com/x/cover/'
# 详情页
detail_url = 'https://v.youku.com/v_show/id_{}.html'
# 为你推荐
recommend_url = 'https://node.video.qq.com/x/vlikecgi/related_rec?rec_num=14&pageContext=page=0&cid={}'
# 评论id接口
comment_id_url = 'https://ncgi.video.qq.com/fcgi-bin/video_comment_id?otype=json&op=3&vid={}'
# 评论接口
comment_url = 'https://video.coral.qq.com/varticle/{}/comment/v2?callback=&orinum=30&oriorder=o&orirepnum=2'
# 分类信息
tags = {

    '公开课': "235",
    #'名人名嘴': "236",
    #'文化': "238",
    #'艺术': "3072",
    #'伦理社会': '3091',
    #'理工': '3092',
    #'历史': '3093',
    #'心理学': '3094',
    # '经济': '动作',
    # '政治': '动作角色扮演',
    # '管理学': "冒险",
    # '外语': "卡牌",
    # '法律': "益智",
    # '计算机': "竞速",
    # '哲学': '模拟经营',
    # '职业培训': '射击',
    # '印度': '养成',
    # '以色列': '对战格斗',
    # '其他': '自然',
    # '教育': '教育',
    # '科技': '科技',
    # '心理': '心理',
    # '家庭教育': '新加坡',
    # '家庭教育': '新加坡',
    # '家庭教育': '新加坡',

}
# mongodb配置
host = '127.0.0.1'  # 主机
port = 27017  # 端口
db = 'media'  # 仓库
collection = 'media'  # 集合
Collection = 'detail_url' # 去重url


tags_1 = {
    '偶像爱情': 1,
    '宫斗权谋': 2,
    '都市生活': 4,
}
tags_2 = {
    '罪案谍战': 5,
    '军旅抗战': 7,
    '喜剧': 8,
}
tags_3 = {
    '玄幻史诗': 3,
    '武侠江湖': 9,
    '青春校园': 10,
    '历险科幻': 6,
}
tags_4 = {
    '时代传奇': 11,
    '体育电竞': 12,
    '真人动漫': 13,
    '当代主旋律': 14,
}
