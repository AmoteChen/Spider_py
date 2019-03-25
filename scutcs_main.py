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

class cs_spider(object):
    def __init__(self):
        print()

    #url 转换为 html
    def getsourse(self,url):
        html=requests.get(url)
        html.encoding='utf-8'
        return html.text
    def changepage(self,total_page):
        header = {
            '__active_paging__': 'listContainer',
            '_page_': '2',
            '__active_region__': 'pageregion',
            '_size_': '15',
            '_': ''
        }
        page_group=[]
        now_url = 'http://cs.scut.edu.cn/newcs/xygk/xytz/index.html?'
        s = requests.session()
        for i in range(1,total_page+1):
            header['_page_']=i
            final = s.get(now_url, params=header)
            page_group.append(final.content.decode())
        return page_group

        # 获取当前月份，以整型变量返回

    def get_system_month(self):
        now_month = int(time.strftime("%m"))
        return now_month

        # 获取当前年份，以整型变量返回

    def get_system_year(self):
        now_year = int(time.strftime("%Y"))
        return now_year

    def get_list(self,page_group):
        lists=re.findall('<li>(.*?)</li>',str(page_group),re.S)
        return lists

    def test_info(self,list):
        final_urls=[]
        original_url='http://cs.scut.edu.cn'
        titles=re.findall('title="(.*?)" target=',list,re.S)
        date=re.findall('class="date">(.*?)</a>',list,re.S)
        month=int(str(date)[7:9])
        year=int(str(date)[2:6])
        te_string='学术报告'
        # print(list)
        if(str(titles).find(te_string)>=0 and cs_spider.get_system_year(self)>=year-1 and month>=cs_spider.get_system_month(self)-1):
            # 筛选条件也要修改
            sub_url=re.findall(r'href="(.*?)" title=',list,re.S)
            # print(sub_url)
            if(str(sub_url[0]).startswith('http:')):
                final_urls.append(str(sub_url[0]))
            else:
                final_url=original_url+str(sub_url[0])
                final_urls.append(str(final_url))
        return final_urls

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
        inner_result=[]
        doc = pq(url=final_url,encoding='utf-8')
        response=doc('.wp_articlecontent .MsoNormal').items()
        for each in response:
            inner_result.append(each.text())
        inner_result.append(final_url)
        final_result=str(inner_result)
        for eachreq in req_list:
            if(final_result.find(eachreq)>=0):
                return inner_result

if __name__ == '__main__':
    final_urls=[]
    req_list=[]
    result_info=[]
    mainspider=cs_spider()
    page_group=mainspider.changepage(3)
    lists=mainspider.get_list(page_group)
    for each in lists:
        final_url=mainspider.test_info(each)
        if(final_url):
            final_urls.append(final_url)
    req_list=mainspider.set_test()
    for each_url in final_urls:
        result_info.append(mainspider.test_result(req_list,each_url[0]))
    if (any(result_info)):
        for eachlist in result_info:
            if(eachlist):
                for each in eachlist:
                    print (each)
            print('\n'*3)

    else:
        print('没有查询到匹配结果')

