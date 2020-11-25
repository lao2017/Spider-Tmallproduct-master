#!/usr/bin/env python
# -*- coding:utf-8 -*-

from gevent import monkey

monkey.patch_all()
import gevent

import datetime
from time import sleep
import proxy_test
import csv

import requests
from urllib import parse
# from utils.utility import get_proxy,printDict
import json
from lxml import etree
from proxy_test import Proxy_start
import re
import warnings

warnings.filterwarnings("ignore")

ps = Proxy_start()
all_set = set()

def get_brand(i, param):
    try:
        print(f"正在采集第{i+1}个分类！\t {param}")
        quote_param = parse.quote(param.encode("gb2312"))
        # print(quote_param)
        url = "https://list.tmall.com/ajax/allBrandShowForGaiBan.htm?t=0&q={}&sort=s&style=g&from=mallfp..pc_1_searchbutton&active=2&spm=875.7931836/B.a2227oh.d100&userIDNum=&tracknick=".format(
            quote_param)
        # https://list.tmall.com/search_product.htm?q=%CA%D6%BB%FA&click_id=%CA%D6%BB%FA&from=mallfp..pc_1.6_hq&spm=875.7931836%2FB.a1z5h.7.66144265FtDHvK
        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "referer": "https://list.tmall.com/search_product.htm?q={}&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton".format(
                quote_param),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
        }
        proxies = ps.get_check_proxy()
        print("proxies : ", proxies)
        response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=10)
        if response.status_code == 200:
            res = response.text.replace('\n', '').replace(' ', '')
            # print("response.text", res)
            if "title" in res:
                #正则title
                content_list = re.findall('({.*?})', res, re.S)
                for content in content_list:
                    title = json.loads(content.replace('\\','/').replace('（','(').replace('）',')').replace('	','')).get('title')
                    print(f"{param} \t title : ", title)
                    # 爬取品牌后带有字母转成小写
                    # all_set.add(title.lower())
                    # 爬取品牌后不用转换大小写，直接写入set
                    all_set.add(title)
        else:
            raise Exception(f"状态码为：{response.status_code}")
    except Exception as e:
        print(e)
        get_brand(i, param)



if __name__ == '__main__':
    all_list = []
    with open("D:/Yuanshiwork/shopping-price-comparison/tb_shangpin_c.txt", encoding="utf-8") as f:
        param_list = f.readlines()
    for cut in range(len(param_list)):
        param_cut = param_list[cut]
        param = param_cut.strip()
        if "/" in param:
            param_lists = param.split("/")
            for param in param_lists:
                all_list.append(param)
        else:
            all_list.append(param)
    # for al in range(93, len(all_list)):
    #     print(f"正在采集第{al+1}个分类！\t {all_list[al]}")
    #     try:
    #         get_brand(all_list[al])
    #     except Exception as e:
    #         print(e)
    #         get_brand(all_list[al])
    #     print("all_set : ", len(all_set))
    task = [gevent.spawn(get_brand, i, all_list[i]) for i in range(len(all_list))]
    gevent.joinall(task)

    print("准备写入。。。", len(all_set))

    with open('D:/Yuanshiwork/shopping-price-comparison/Tianmao.txt', 'a+') as csv_file:
        for as_ in list(all_set):
            csv_file.write(as_+"\n")
