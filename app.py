from flask import Flask ,render_template
from flask import url_for
from flask import request
from flask import redirect
import string

import requests
import re
import time
import sys
import io
import codecs
from pyquery import PyQuery as pq
import PK__Spider

import jiaotong_spider
import LOLS_spider
import huanong_spider
import jinan_spider
import qinghua_spider
import scutcs_main
import scutse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
app = Flask(__name__)
def cleaner(list) :
    list=[]
    return list

@app.route('/', methods=["POST","GET"])
def index():
    return render_template("index.html")
@app.route('/selectpage',methods=["POST","GET"])
def selectpage():
    return render_template('selectpage.html')
@app.route('/scutse',methods=["POST","GET"])
def scutse1():
    classinfo = []
    descriptions = []
    final_info = []
    url = 'http://www2.scut.edu.cn/sse/xshd/list1.htm'
    mainspider = scutse.scut_spider()
    all_links = mainspider.changepage(url, 3)

    for link in all_links:
        html = mainspider.getsourse(link)
        everylist = mainspider.get_list(html)

        for each in everylist:
            info = mainspider.get_info(each)
            if (mainspider.test_info(info)):
                classinfo.append(info)
    all_urls = mainspider.get_total_url(classinfo)

    for to_url in all_urls:
        descriptions.append(mainspider.get_descp(to_url))
    req_list= []

    if request.method == 'POST':
            a=request.form['scutse1']
            b=request.form['scutse2']
            c=request.form['scutse3']
            d=request.form['scutse4']
            e=request.form['scutse5']
            if a :
                req_list.append(a)
            if b:
                req_list.append(b)
            if c :
                req_list.append(c)
            if d :
                req_list.append(d)
            if e :
                req_list.append(e)

            if not req_list:
                return redirect(url_for('errorpage'))
            for each in descriptions:
                if mainspider.test_descp(req_list, str(each)) > 0:
                    final_info.append(each)
                else:
                    continue
            return render_template('scutse.html', resultlist_se=final_info, test_list_se=req_list)
    return render_template('scutse.html')

@app.route('/scutcs',methods=["POST","GET"])
def scutcs():
    final_urls = []
    result_info = []
    mainspider_cs = scutcs_main.cs_spider()
    page_group = mainspider_cs.changepage(3)
    lists = mainspider_cs.get_list(page_group)
    for each in lists:
        final_url = mainspider_cs.test_info(each)
        if (final_url):
            final_urls.append(final_url)

    req_list_cs= []

    if request.method == 'POST':
            a=request.form['scutcs1']
            b=request.form['scutcs2']
            c=request.form['scutcs3']
            d=request.form['scutcs4']
            e=request.form['scutcs5']
            if a :
                req_list_cs.append(a)
            if b:
                req_list_cs.append(b)
            if c :
                req_list_cs.append(c)
            if d :
                req_list_cs.append(d)
            if e :
                req_list_cs.append(e)

            if not req_list_cs:
                return redirect(url_for('errorpage'))

            result_info=shaixuan_cs(final_urls,req_list_cs,result_info,mainspider_cs)
            return render_template('scutcs.html', resultlist_cs=result_info,test_list_cs=req_list_cs)
    return render_template('scutcs.html')
def shaixuan_cs(final_urls,req_list_cs,result_info,mainspider_cs):
    for each_url in final_urls:
        result_info.append(mainspider_cs.test_result(req_list_cs,each_url[0]))
    return result_info
@app.route('/beida',methods=["POST","GET"])
def beida():

    mainspider = PK__Spider.pk_spider()
    final_urls = []
    result_info = []

    page_group = mainspider.changepage(3)
    for each in page_group:
        lists = mainspider.get_list(each)
        for each in lists:
            if (mainspider.test_info(str(each))):
                final_urls.append(mainspider.test_info(str(each)))

    req_lists=[]

    if request.method == 'POST':
            a=request.form['beida1']
            b=request.form['beida2']
            c=request.form['beida3']
            d=request.form['beida4']
            e=request.form['beida5']
            if a :
                req_lists.append(a)
            if b:
                req_lists.append(b)
            if c :
                req_lists.append(c)
            if d :
                req_lists.append(d)
            if e :
                req_lists.append(e)

            if not req_lists:
                return redirect(url_for('errorpage'))

            result_info = paqu(final_urls,req_lists,result_info,mainspider)

            return render_template('beida.html', resultlist1=result_info,test_list=req_lists)

    return render_template('beida.html')
def paqu(final_urls,req_lists,result_info,mainspider):
    for each_url in final_urls:
        result_info.append(mainspider.test_result(req_lists,each_url))
    return result_info
@app.route('/qinghua',methods=["POST","GET"])
def qinghua():
    mainspider_qinghua = qinghua_spider.tr_spider()
    final_urls = []
    result_info = []
    page_group = mainspider_qinghua.changepage(3)
    for each in page_group:
        lists = mainspider_qinghua.get_list(each)
        for each in lists:
            if (mainspider_qinghua.test_info(str(each))):
                final_urls.append(mainspider_qinghua.test_info(str(each)))
    req_list_qinghua= []
    if request.method == 'POST':
            a=request.form['qinghua1']
            b=request.form['qinghua2']
            c=request.form['qinghua3']
            d=request.form['qinghua4']
            e=request.form['qinghua5']
            if a :
                req_list_qinghua.append(a)
            if b:
                req_list_qinghua.append(b)
            if c :
                req_list_qinghua.append(c)
            if d :
                req_list_qinghua.append(d)
            if e :
                req_list_qinghua.append(e)

            if not req_list_qinghua:
                return redirect(url_for('errorpage'))

            result_info= shaixuan_qinghua(final_urls,req_list_qinghua,result_info,mainspider_qinghua)

            return render_template('qinghua.html',resultlist_qinghua=result_info,test_list_qinghua=req_list_qinghua)
    return render_template('qinghua.html')
def shaixuan_qinghua(final_urls,req_list_qinghua,result_info,mainspider_qinghua):
    for each in final_urls:
        result_info.append(mainspider_qinghua.test_result(req_list_qinghua, each))
    return result_info
@app.route('/jinan',methods=["POST","GET"])
def jinan():
    JN_spider = jinan_spider.jn_spider()
    req_list = []
    result_info = []
    final_urls = []
    page_group = JN_spider.changepage(3)
    for each in page_group:
        lists = JN_spider.get_list(each)
        for each in lists:
            if (JN_spider.test_info(str(each))):
                final_urls.append(JN_spider.test_info(str(each)))
    req_lists = []
    if request.method == 'POST':
            a=request.form['jinan1']
            b=request.form['jinan2']
            c=request.form['jinan3']
            d=request.form['jinan4']
            e=request.form['jinan5']
            if a :
                req_lists.append(a)
            if b:
                req_lists.append(b)
            if c :
                req_lists.append(c)
            if d :
                req_lists.append(d)
            if e :
                req_lists.append(e)

            if not req_lists:
                return redirect(url_for('errorpage'))

            result_info = shaixuan_jinan(final_urls,req_lists,result_info,JN_spider)

            return render_template('jinan.html', resultlist_jinan=result_info,test_list_jinan=req_lists)
    return render_template('jinan.html')
def shaixuan_jinan(final_urls,req_lists,result_info,JN_spider) :
    for each in final_urls:
        result_info.append(JN_spider.test_result(req_lists, each))
    return result_info
@app.route('/jiaotong',methods=["POST","GET"])

def jiaotong():
    mainspider1 = jiaotong_spider.sj_spider()
    final_urls = []
    result_info1 = []
    lists = mainspider1.get_list(3)
    for each in lists:
        if (mainspider1.test_info(str(each))):
            final_urls.append(mainspider1.test_info(str(each)))

    req_lists = []

    if request.method == 'POST':
        a = request.form['jiaotong1']
        b = request.form['jiaotong2']
        c = request.form['jiaotong3']
        d = request.form['jiaotong4']
        e = request.form['jiaotong5']
        if a:
            req_lists.append(a)
        if b:
            req_lists.append(b)
        if c:
            req_lists.append(c)
        if d:
            req_lists.append(d)
        if e:
            req_lists.append(e)

        if not req_lists:
            return redirect(url_for('errorpage'))

        result_info1 = shaixuan(final_urls, req_lists, result_info1, mainspider1)

        return render_template('jiaotong.html', resultlist2=result_info1, test_list2=req_lists,test_list3=final_urls)
    return render_template('jiaotong.html')


def shaixuan(final_urls, req_lists, result_info1, mainspider1):
    for each_url in final_urls:
        result_info1.append(mainspider1.test_result(req_lists, each_url))
    return result_info1



@app.route('/huanong',methods=["POST","GET"])
def huanong():
    mainspider2 = huanong_spider.hn_spider()
    page_group = []
    final_urls = []
    result_info2 = []
    page_group = mainspider2.changepage(3)
    for each in page_group:
        lists = mainspider2.get_list(each)
        for each in lists:
            if (mainspider2.test_info(str(each))):
                final_urls.append(mainspider2.test_info(str(each)))
    req_lists=[]

    if request.method == 'POST':
        a = request.form['huanong1']
        b = request.form['huanong2']
        c = request.form['huanong3']
        d = request.form['huanong4']
        e = request.form['huanong5']
        if a:
            req_lists.append(a)
        if b:
            req_lists.append(b)
        if c:
            req_lists.append(c)
        if d:
            req_lists.append(d)
        if e:
            req_lists.append(e)

        if not req_lists:
            return redirect(url_for('errorpage'))

        result_info2 = shaixuan_huanong(final_urls, req_lists, result_info2, mainspider2)
        return render_template('huanong.html', resultlist3=result_info2, test_list3=req_lists)
    return render_template('huanong.html')

def shaixuan_huanong(final_urls, req_lists, result_info2, mainspider2):
    for each in final_urls:
        result_info2.append(mainspider2.test_result(req_lists, each))
    return result_info2
@app.route('/guojia',methods=["POST","GET"])
def guojia():
    mainspider_guojia = LOLS_spider.lols_spider()
    final_urls_guojia = []
    result_info_guojia = []
    page = 'http://sklois.iie.cas.cn/xwzx/tzgg/index.html'
    lists = mainspider_guojia.get_list(page)
    for each in lists:
        if (mainspider_guojia.test_info(str(each))):
            final_urls_guojia.append(mainspider_guojia.test_info(str(each)))
    req_lists_guojia= []
    if request.method == 'POST':
        a = request.form['guojia1']
        b = request.form['guojia2']
        c = request.form['guojia3']
        d = request.form['guojia4']
        e = request.form['guojia5']
        if a:
            req_lists_guojia.append(a)
        if b:
            req_lists_guojia.append(b)
        if c:
            req_lists_guojia.append(c)
        if d:
            req_lists_guojia.append(d)
        if e:
            req_lists_guojia.append(e)

        if not req_lists_guojia:
            return redirect(url_for('errorpage'))

        result_info_guojia = shaixuan_guojia(final_urls_guojia, req_lists_guojia, result_info_guojia, mainspider_guojia)
        return render_template('guojia.html', resultlist_guojia=result_info_guojia, test_list_guojia=req_lists_guojia)
    return render_template('guojia.html')

def shaixuan_guojia(final_urls_guojia, req_lists_guojia, result_info_guojia, mainspider_guojia):
    for each in final_urls_guojia:
        result_info_guojia.append(mainspider_guojia.test_result(req_lists_guojia, each))
    return result_info_guojia



@app.route('/errorpage',methods=["POST","GET"])
def errorpage():
    return render_template('errorpage.html')


if __name__ == '__main__':
    app.run()
