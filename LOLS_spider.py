# -*- coding:utf8 -*-
import string

import requests
import re
import time
import sys
import io
import codecs
from pyquery import PyQuery as pq



class lols_spider(object):
    def __init__(self):
        print()

    def getsourse(self, url):
        html = requests.get(url)
        html.encoding = 'utf-8'
        return html.text

    def get_system_month(self):
        now_month = int(time.strftime("%m"))
        return now_month

        # 获取当前年份，以整型变量返回

    def get_system_year(self):
        now_year = int(time.strftime("%Y"))
        return now_year

    def get_list(self,source):
        lists=[]
        doc=pq(url=source,encoding='utf-8')
        responses=doc('.news_list.margin20 li').items()
        for response in responses:
            lists.append(response)
        return lists

    def test_info(self, string):
        original_url='http://sklois.iie.cas.cn/xwzx/tzgg'
        te_string='学术报告'
        date=re.findall(r'<li><span>(.*?)</span>',string,re.S)
        sub_url=re.findall('href="(.*?)">',string,re.S)
        title=re.findall('">(.*?)</a></li>',string,re.S)
        year = int(str(date[0])[1:5])
        if(str(title).find(te_string)>=0 and year>=lols_spider.get_system_year(self)-2):
            # 筛选条件根据实际情况可以变更
            final_url=original_url+str(sub_url[0])[1:]
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

    def test_result(self,req_list,final_url):
        inner_result = []
        doc = pq(url=final_url, encoding='utf-8')
        response = doc('.center1000 .article_con .TRS_Editor p').items()
        for each in response:
            inner_result.append(each.text())
        inner_result.append(final_url)
        final_result = str(inner_result)
        for eachreq in req_list:
            if (final_result.find(eachreq) >= 0):
                return inner_result

'''
if __name__=='__main__':
    mainspider=lols_spider()
    final_urls=[]
    result_info = []
    page='http://sklois.iie.cas.cn/xwzx/tzgg/index.html'
    lists=mainspider.get_list(page)
    for each in lists:
        if (mainspider.test_info(str(each))):
            final_urls.append(mainspider.test_info(str(each)))
    req_list = mainspider.set_test()
    for each in final_urls:
        result_info.append(mainspider.test_result(req_list,each))
    if (any(result_info)):
        for eachlist in result_info:
            if (eachlist):
                for each in eachlist:
                    print(str(each).replace('\n',''))
        print('\n'*3)
    else:
        print('没有查询到匹配结果')
'''