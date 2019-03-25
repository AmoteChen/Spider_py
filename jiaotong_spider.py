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

class sj_spider(object):
    def __init__(self):
        print()

    def getsourse(self,url):
        html=requests.get(url)
        html.encoding='utf-8'
        return html.text

    def get_system_month(self):
        now_month = int(time.strftime("%m"))
        return now_month

        # 获取当前年份，以整型变量返回

    def get_system_year(self):
        now_year = int(time.strftime("%Y"))
        return now_year

    def get_list(self,total_page):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '1004',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'www.cs.sjtu.edu.cn',
            'Origin': 'http://www.cs.sjtu.edu.cn',
            'Refere': 'http://www.cs.sjtu.edu.cn/NewNotice.aspx',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        data = {'__EVENTTARGET': 'AspNetPager1',
                '__EVENTARGUMENT': '2',
                # '__VIEWSTATE': '',
                # '__EVENTVALIDATION': '',
                # 'Top$Textbox1': '',
                # 'AspNetPager1_input': '',
                # 'RightPath$DropDownList1':'27',
                # 'RightPath$DropDownList2':'2'
                }
        lists = []
        now_url = 'http://www.cs.sjtu.edu.cn/NewNotice.aspx'
        r = requests.session()
        for i in range(1, total_page + 1):
            data['__EVENTARGUMENT'] = i
            final = r.post(now_url, data=data, headers=header)
            doc = pq(final.content.decode('utf-8'))
            responses = doc('.Main .NewsList ul li').items()
            for response in responses:
                lists.append(response)
        return lists

    def test_info(self,string):
        original_url='http://www.cs.sjtu.edu.cn/'
        te_string = '讲座'
        date=re.findall(r'\n                                (.*?)</span>',string,re.S)
        title=re.findall('</span>(.*?)</a>',string,re.S)
        sub_url=re.findall('<a href="(.*?)">',string,re.S)
        month = int(str(date[0])[5:7])
        year = int(str(date[0])[0:4])
        if (str(title[0]).find(te_string)>=0 and year >= sj_spider.get_system_year(self)-1 and month >= sj_spider.get_system_month(self) - 7):
            # 筛选条件根据实际情况可以变更
            final_url = original_url + str(sub_url[0])
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
        response = doc('.Container .p20.lh250').items()
        for each in response:
            inner_result.append(each.text())
        inner_result.append(final_url)
        final_result = str(inner_result)
        for eachreq in req_list:
            if (final_result.find(eachreq) >= 0):
                return inner_result

if __name__=='__main__':
    mainspider=sj_spider()
    final_urls=[]
    result_info = []
    lists=mainspider.get_list(3)
    # for each in lists:
    #     print(each)
    for each in lists:
        if (mainspider.test_info(str(each))):
            final_urls.append(mainspider.test_info(str(each)))
    req_list = mainspider.set_test()
    for each in final_urls:
        result_info.append(mainspider.test_result(req_list, each))
    if (any(result_info)):
        for eachlist in result_info:
            if (eachlist):
                for each in eachlist:
                    print(each)
            print('\n'*3)
    else:
        print('没有查询到匹配结果')