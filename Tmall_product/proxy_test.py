#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 代理池  2018.5.22


# from sswang.logging_app import *
import urllib.request
import time
import re


class Proxy_start(object):
    def __init__(self):
        try:
            # logger.info("启动代理池，初始化。")
            self.proxy_url = '添加自己的云代理'
           
            # self.proxy_list = ['1.1.1.1:57112']
            self.proxy_list = [proxy for proxy in
                               urllib.request.urlopen(self.proxy_url).read().decode("utf-8").split("\r\n")]
            self.proxy_list.pop()
            # logger.info("代理池，初始化完成。")
        except Exception as e:
            # logger.info("代理池，初始化异常---> %s" % e)
            # logger.info("代理池，10秒后重启，请等待。。。")
            time.sleep(10)
            self.__init__()

    # 获取代理
    def get_proxy_list(self):
        try:
            pro_list = [proxy for proxy in urllib.request.urlopen(self.proxy_url).read().decode("utf-8").split("\r\n")]
            pro_list.pop()
            # logger.info("API 获取代理成功！数量：%s" % len(pro_list))
            return pro_list
        except Exception as e:
            # logger.info("获取代理异常！, %s " % e)
            self.get_proxy_list()

    # 添加代理
    def add_proxy(self):
        try:
            if len(self.proxy_list) < 100:
                result_get_proxy = self.get_proxy_list()
                # logger.info("添加前 self.proxy_list 数量：%s" % len(self.proxy_list))
                for pro in result_get_proxy:
                    if len(pro) == 0:
                        continue
                    if pro in self.proxy_list:
                        # logger.info("API 添加代理重复！数量：%s" % pro)
                        continue
                    self.proxy_list.insert(0, pro)
                    # logger.info("API 添加代理成功！数量：%s" % pro)
                for pro_s in self.proxy_list:
                    if pro_s not in result_get_proxy:
                        self.proxy_list.remove(pro_s)
                        # logger.info("添加后 self.proxy_list 数量：%s" % len(self.proxy_list))
            return self.proxy_list
        except Exception as e:
            # logger.info("添加代理异常！, %s" % e)
            return self.proxy_list
            # print(self.proxy_list)

    # 轮询代理
    def get_proxy(self):
        # print("代理池IP数量：%s" % len(self.proxy_list))
        try:
            self.proxy_list = self.add_proxy()
            # logger.info("代理池IP数量：%s" % len(self.proxy_list))
            proxy = self.proxy_list[-1]
            self.proxy_list.remove(proxy)
            self.proxy_list.insert(0, proxy)
            # logger.info("调用代理成功！,%s" % proxy)
            return proxy
        except Exception as e:
            # logger.info("调用代理异常！,%s" % e)
            self.get_proxy()

    # 删除代理
    def delete_proxy(self, proxy):
        try:
            for proxies in self.proxy_list:
                try:
                    result = re.search('(' + proxy + ')', proxies).group(1)
                    if result:
                        self.proxy_list.remove(proxies)
                        # logger.info("删除代理成功！,%s" % proxies)
                        return "delete_proxy 成功!"
                except:
                    pass

            return "delete_proxy 失败!"
        except Exception as e:
            # logger.info("删除代理异常！,%s" % e)
            return "delete_proxy 失败!"


    # 获取代理
    def get_check_proxy(self):
        complete_proxy = self.proxy_time()
        ip_port = complete_proxy.split(",")[0].split(":")
        ip = ip_port[0]
        port = ip_port[1]
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": ip,
            "port": port,
            "user": "yuanshi1",
            "pass": "yuanshi1",
        }
        proxyMetas = "https://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": ip,
            "port": port,
            "user": "yuanshi1",
            "pass": "yuanshi1",
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMetas,
        }
        # logger.info("proxyType: %s proxyMeta: %s complete_proxy: %s" % (proxyType, proxies, complete_proxy))
        return proxies

    # 检测代理有效时间
    def proxy_time(self):
        while True:
            complete_proxy = self.get_proxy()
            proxy_end_time = int(complete_proxy.split(",")[-1])
            if proxy_end_time - time.time() >= 60:
                # logger.info("代理可用时间 大 15秒 %s" % complete_proxy)
                break
            # logger.info("代理可用时间 小 15秒 %s" % complete_proxy)
            error_ip = complete_proxy.split(",")[0]
            error_msg = self.delete_proxy(error_ip)
            # logger.info("代理可用时间 删除 %s ，返回结果: %s " % (error_ip, error_msg))
        return complete_proxy

    # 获取所有的代理IP
    def get_all_proxy(self):
        return self.proxy_list

# if __name__ == '__main__':
#     try:
#         pro = Proxy_start()
#     except Exception as e:
#         logger.info("启动main方法异常: %s" % e)
#         pro = Proxy_start()
#     while True:
#         try:
#             pro.add_proxy()
#         except Exception as e:
#             logger.info("循环检测代理异常: %s" % e)
#         time.sleep(10)


# def test_proxy(self):
#     baidu_url = "https://ip.cn/"
#     for ip_port in self.proxy_list:
#         time.sleep(2)
#         proxy = {
#             "https": "https://{}".format(ip_port),
#             "http": "http://{}".format(ip_port)
#         }
#         # print(proxy)
#         try:
#             response = requests.get(baidu_url,verify=False,timeout=5,proxies=proxy)
#             wy_ip = response.text.replace("\n", "")
#             # print(response.status_code)
#             if response.status_code == 200 and wy_ip == ip_port.split(":")[0]:
#                 logger.info("有效的IP: %s" % ip_port)
#                 continue
#         except Exception as e:
#             self.proxy_list.remove(ip_port)
#             logger.info("已删除无效IP: %s" % ip_port)
#             # print("已删除无效IP:",ip_port)


# f = open("product.txt","r",encoding = "utf-8")   #设置文件对象
# line = f.readline()
# line = line[:-1]
# while line:             #直到读取完文件
#     line = f.readline()  #读取一行文件，包括换行符
#     line = line[:-1]     #去掉换行符，也可以不去
#     print(line)
# f.close() #关闭文件