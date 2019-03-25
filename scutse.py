




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


class scut_spider(object):
    def __init__(self):
        print()

    # url转换为html
    def getsourse(self,url):
        html=requests.get(url)
        html.encoding='utf-8'
        return html.text

    #用于华工学术活动网页翻页处理
    def changepage(self,url,total_page):
        now_page=int(re.search('list(\d+)',url,re.S).group(1))
        page_group=[]
        for i in range(now_page,total_page+1):
            link=re.sub('list(\d+)','list%s'%i,url,re.S)
            page_group.append(link)
        return page_group

    #获取当前月份，以整型变量返回
    def get_system_month(self):
        now_month=int(time.strftime("%m"))
        return now_month

    #获取当前年份，以整型变量返回
    def get_system_year(self):
        now_year = int(time.strftime("%Y"))
        return now_year

    # 用于检验list中信息是否符合要求
    def test_info(self,eachinfo):
        if (int(eachinfo['year']) == scut_spider.get_system_year(self)) and (int(eachinfo['month']) >= (scut_spider.get_system_month(self)) - 3):
            te_string='学术报告'
            if(eachinfo['title'].find(te_string)>=0):
                return True
            else:
                return False

    # 将List中项目的子url拼接成目标url
    def link_url(self,eachinfo):
        basic_url='www2.scut.edu.cn'
        total_url='http://'+basic_url+eachinfo.get('sub_url')
        return total_url

    #爬去网站通知列表中的时间，以list格式返回
    def get_list(self,source):
        lists=re.findall('(news_li">(.*?)</li>)',source,re.S)
        return lists

    def get_descp(self,to_url):
        all_responses=[]
        doc = pq(url=to_url, encoding='utf-8')
        response = doc('.wp_articlecontent .western').items()
        for each in response:
            all_responses.append(each.text())
        all_responses.append(to_url)
        return all_responses

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

    def test_descp(self,req_list,each_descp):
        count=0
        for each in req_list:
            if(each_descp.find(each)>=0):
                count+=1
        return count

    def get_info(self,eachlist):
        info={}
        info['title']=str(re.search(r'title=\\\'(.*?)\\\'>',str(eachlist),re.S).group(1))
        info['sub_url']=str(re.search(r'<a href=\\\'(.*?)\\\' target=',str(eachlist),re.S).group(1))
        info['total_url']=scut_spider().link_url(info)
        # 先把list转换为str类型
        time_str=''.join(re.search('news_meta">(.*?)</span>',str(eachlist),re.S).group(1))
        # 截取出年和月
        year_str = time_str[0:4]
        month_str = time_str[5:7]

        info['year']=year_str
        info['month']=month_str
        return info

    def get_total_url(self,classinfo):
        t_url=[]
        length =len(classinfo)
        for index in range(length):
            t_url.append(classinfo[index]['total_url'])

        return t_url


if __name__ == '__main__':
    classinfo=[]
    descriptions=[]
    final_info=[]
    url='http://www2.scut.edu.cn/sse/xshd/list1.htm'
    mainspider=scut_spider()
    all_links=mainspider.changepage(url,3)

    for link in all_links:
        html=mainspider.getsourse(link)
        everylist=mainspider.get_list(html)

        for each in everylist:
            info=mainspider.get_info(each)
            if(mainspider.test_info(info)):
                classinfo.append(info)
    all_urls=mainspider.get_total_url(classinfo)

    for to_url in all_urls:
        descriptions.append(mainspider.get_descp(to_url))

    re_list=mainspider.set_test()
    # print(re_list)

    for each in descriptions:
        if mainspider.test_descp(re_list, str(each))>0:
            final_info.append(each)
        else:
           continue
    if(final_info):
        for each_item in final_info:
            for each in each_item:
                print(each)
    else:print('没有查询到匹配结果')
    # for each in descriptions:
    #     print(each)







# html =requests.get('http://www2.scut.edu.cn/sse/xshd/list.htm')
# html.encoding='utf-8'
# time = re.findall('"news_meta">(.*?)</span>',html.text,re.S)
# print(time)
# # print(html.text)
