# -*- coding: utf-8 -*-

import sys
import time
import json
import re

# tags_json_str = {"key_cat": "", "衣长": "中长款", "风格": "欧美;街头", "领子": "V领", "袖长": "长袖", "key_scene": "春秋季", "风格二级": "欧美", "key_body": "宽松型", "图案": "纯色", "材质": "腈纶", "key_human": "", "款式": "开衫", "组合形式": "单件", "颜色分类": ""}
# #print tags_json_str
# tags_json = json.dumps(tags_json_str)
# print tags_json
# tags_json = json.loads(tags_json)
# 
# tmp_tags = []
# for tag in tags_json:
#     tmp_tags.append(tag + '_' + tags_json[tag])
#     tags_json_temp = ','.join(tmp_tags)
# print tags_json_temp


# query_score_dict={'1008_25_休闲_夏': 4, '1008_17_通勤_夏': 4, '1008_5_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_17_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_21_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_20_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_25_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_21_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_23_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_19_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_20_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_17_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_18_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_19_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_5_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_16_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_21_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_5_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_23_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_16_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_21_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_23_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_23_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_25_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_18_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_19_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_18_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_20_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_19_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_5_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_25_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_17_\xe7\xae\x80\xe7\xba\xa6_\xe5\xa4\x8f': 4, '1008_16_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4, '1008_20_\xe9\x80\x9a\xe5\x8b\xa4_\xe5\xa4\x8f': 4, '1008_16_\xe4\xbc\x91\xe9\x97\xb2_\xe5\xa4\x8f': 4, '1008_18_\xe7\x94\x9c\xe7\xbe\x8e_\xe5\xa4\x8f': 4}
# a = dict()
# for key,value in query_score_dict.iteritems():
#     print key.decode("utf-8")
#     a[key.decode("utf-8").encode('utf-8')] = value
# print a

# with open("D:/workspace/test/conf/socket_match_dict.conf", "r") as fi:
#     conf_content = fi.read()
#     socket_match_dict = eval(conf_content) 
#     print socket_match_dict
#       
#     socket_cat_match_dict = dict()
#       
#     for key,value in socket_match_dict.iteritems():
#         match_list_str = str(value)
#         match_set = set(match_list_str.split("|"))
#           
#         socket_cat_pair_list_str = key
#         socket_cat_pair_list = socket_cat_pair_list_str.split('|')
#   
#         for socket_cat_key in socket_cat_pair_list:
#             tmp_match_set = socket_cat_match_dict.get(socket_cat_key, set())
#             
#             print "match_set:%s--socket_cat_key:%s--tmp_match_set:%s"  % (match_set,socket_cat_key,tmp_match_set)
# 
#             time.sleep(1)
#               
#             tmp_match_set |= match_set
#             print tmp_match_set
#             socket_cat_match_dict[socket_cat_key] = tmp_match_set
#             print "=================="
      


# s = "../data/test.jpg"
# pos = s.rfind("/")
# print pos
# print s[pos+1]
# 
# print [1,2,3,4,5,6][0:-1]

def zhengze():
    str = '(cat_id:161 AND tags_json:裤长_长裤 AND tags_json:裤型_直筒裤 AND (tags_json:材质_纯棉 OR tags_json:材质_棉麻 OR tags_json:材质_亚麻 OR tags_json:材质_棉质 OR tags_json:材质_全棉 OR tags_json:材质_莱卡棉 OR tags_json:材质_织锦 OR tags_json:材质_棉 OR tags_json:材质_螺纹棉) AND tags_json:key_tag_修身) AND (cat_id:161 OR tags_json:腰型_中腰^100)'
    tags = re.findall(r'(?<=tags_json:).*?(?=[ \(\)A|^])',str)
    print tags
    tmptag = ','.join(tags)
    print tmptag
    for tag in tags:
        print tag.encode('utf-8')
    
def filter_test(x):
    return x%2 != 0

print filter(filter_test, range(1,20))

def map_test(x):
    return x*x
print map(map_test, range(1,10))

def reduce_test(x):
    return x * x

print reduce(reduce_test, [range(1,10)])
                    
if __name__ == '__main__':
    pass
    #zhengze()

