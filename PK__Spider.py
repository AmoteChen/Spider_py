# -*- coding:utf8 -*-
import string

import requests
import re
import time
import sys
import io
import codecs
from pyquery import PyQuery as pq

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
class pk_spider(object):

    def __init__(self):
        print()

    def getsourse(self, url):
        html = requests.get(url)
        html.encoding = 'utf-8'
        return html.text

    def changepage(self, total_page):
        page_group = []
        now_url = 'http://eecs.pku.edu.cn/Survey/Lecture/?PageID=0'
        for i in range(1, total_page + 1):
            link = re.sub("PageID=\d+", 'PageID=%s' %(i-1), now_url, re.S)
            page_group.append(link)
        return page_group

    def get_system_month(self):
        now_month = int(time.strftime("%m"))
        return now_month

        # 获取当前年份，以整型变量返回

    def get_system_year(self):
        now_year = int(time.strftime("%Y"))
        return now_year

    def get_list(self,source):
        lists=[]
        doc=pq(url=source)
        responses=doc('.content .ggtzM li').items()
        for response in responses:
            lists.append(response)
        return lists

    def test_info(self, string):
        original_url='http://eecs.pku.edu.cn/Survey/Lecture/'
        date=re.findall('<em>(.*?)</em>',string,re.S)
        sub_url=re.findall('href="(.*?)">',string,re.S)
        month = int(str(date[0])[5:7])
        year = int(str(date[0])[0:4])
        if(year>=pk_spider.get_system_year(self)-1 and month>=pk_spider.get_system_month(self)-2):
            # 筛选条件根据实际情况可以变更
            final_url=original_url+str(sub_url[0])
            return final_url

    def set_test(self):
        req_list = []
        print('请输入多个筛选条件（最多5个，以‘#’表示最后一个）' + '\n')
        for index in range(1, 5):
            print('请输入第' + str(index) + '个筛选条件：')
            req = input()
            if (req != '#'):
                req_list.append(req)
            else:
                break
        return req_list


    def test_result(self, req_list, final_url):
        inner_result = []
        doc = pq(url=final_url, encoding='utf-8')
        response1 = doc('.content .neiyeMh1').items()
        for each in response1:
            inner_result.append(each.text())
        response2 = doc('.content .neiyeMnr p').items()
        for each in response2:
            inner_result.append(each.text())
        inner_result.append(final_url)
        final_result = str(inner_result)
        for eachreq in req_list:
            if (final_result.find(eachreq) >= 0):
                return inner_result

if __name__=='__main__':
    mainspider=pk_spider()
    final_urls = []
    result_info = []
    page_group=mainspider.changepage(3)
    for each in page_group:
        lists=mainspider.get_list(each)
        for each in lists:
            if (mainspider.test_info(str(each))):
                final_urls.append(mainspider.test_info(str(each)))
    req_list = mainspider.set_test()
    for each_url in final_urls:
        result_info.append(mainspider.test_result(req_list,each_url))
    if (any(result_info)):
        for eachlist in result_info:
            if (eachlist):
                for each in eachlist:
                    print (each)
            print('\n'*3)

    else:
        print('没有查询到匹配结果')
