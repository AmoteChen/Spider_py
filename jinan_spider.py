# -*- coding:utf8 -*-
import string

import requests
import re
import time
import sys
import io
import codecs
from pyquery import PyQuery as pq

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class jn_spider(object):
    def __init__(self):
        print()
    # url 转换为 html

    def getsourse(self, url):
        html = requests.get(url)
        html.encoding = 'utf-8'
        return html.text

    def changepage(self,total_page):
        page_group=[]
        now_url='https://xxxy.jnu.edu.cn/Category_37/Index_1.aspx'
        for i in range(1,total_page+1):
            link=re.sub('Index_\d+','Index_%s'%i,now_url,re.S)
            page_group.append(link)
        return page_group

        # 获取当前月份，以整型变量返回

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
        resposes=doc('#mainContent .newsList li').items()
        for respose in resposes:
            lists.append(respose)
        return lists

    def test_info(self,string):
        original_url='https://xxxy.jnu.edu.cn'
        te_string='学术讲座'
        titles=re.findall('title="标题：(.*?)&#13',string,re.S)
        date=re.findall('class="date">(.*?)</span>',string,re.S)
        sub_url=re.findall('<a href="(.*?)" target=',string,re.S)
        if(date):
            month = int(str(date)[7:9])
            year = int(str(date)[2:6])
        if(str(titles).find(te_string)>=0 and jn_spider.get_system_year(self)==year and month>=jn_spider.get_system_month(self)-2):
#             筛选条件根据实际情况可以变更
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

    def test_result(self,req_list,final_url):
        inner_result = []
        doc = pq(url=final_url, encoding='utf-8')
        response = doc('.conTxt').items()
        for each in response:
            inner_result.append(each.text())
        inner_result.append(final_url)
        final_result = str(inner_result)
        for eachreq in req_list:
            if (final_result.find(eachreq) >= 0):
                return inner_result

if __name__ == '__main__':
    JN_spider=jn_spider()
    req_list=[]
    result_info=[]
    final_urls=[]
    page_group=JN_spider.changepage(3)
    for each in page_group:
        lists=JN_spider.get_list(each)
        for each in lists:
            if(JN_spider.test_info(str(each))):
                final_urls.append(JN_spider.test_info(str(each)))
    req_list = JN_spider.set_test()
    for each in final_urls:
        result_info.append(JN_spider.test_result(req_list, each))
    if(any(result_info)):
        for eachlist in result_info:
            if(eachlist):
                for each in eachlist:
                    print (each)
            print('\n'*3)
    else:
        print('没有查询到匹配结果')


