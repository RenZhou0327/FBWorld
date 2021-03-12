# -*- coding:utf-8 -*-
from Queue import Queue
import threading
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import time
import urllib
import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

def valid_filename(s):
    import string
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    s = ''.join(c for c in s if c in valid_chars)
    return s


def get_page(page):
    try:
        f = urllib2.urlopen(page,timeout=2.0)
        html=f.read()
    except Exception, err:
        print err
        return None
    return html



def get_all_links0(content, page):
    links = []
    soup=BeautifulSoup(content,'html.parser')
    urls=soup.findAll('a',{'href':re.compile('^http|^/')})
    for i in urls:
        u = (i.get('href'))
        if(not re.match('^http',u)):
            u = urlparse.urljoin(page,u)
        if (len(u) > 5 and u != page and u not in crawled):
            links.append(u)
    return links

def get_all_links(content, page):
    links = []
    res1 = r'<a.*?href=.*?<\/a>'
    res2 = r'href=".*?"'
    a = re.findall(res1, content, re.I|re.M|re.S)
    for i in a:
        url = re.findall(res2, i, re.I|re.M|re.S)
        if (url):
            url = url[0].split('"')[1]
        if (len(url) > 4 and url[0] != '#'):
            if re.match('^//', url):#如果url以//开头
                url = 'https:' + url
            elif re.match('^/', url):
                url = page + url
            if re.match('.*/$', url):
                url = url[:-1]#删去最后的/
            if url[:4] == 'http':
                links.append(url)
    return links

def get_all_linksforsports(content, page):
    sportslinks = []
    #res1 = r'item.jd.com.*\.html$'
    urls = re.findall(r"http://sports.sina.com.cn/go.*?.shtml|https://sports.sina.com.cn/go.*?.shtml",content,re.I)#https://sports.sina.com.cn/china/j/2019-12-13/doc-iihnzahi7174738.shtml
    #url1=re.findall(r"http://sports.sina.com.cn/csl/.+.shtml",content,re.I)
    for u in urls:
        sportslinks.append(u)
    return sportslinks

def add_page_to_folder(page, content):  # 将网页存到文件夹里，将网址和对应的文件名写入index.txt中^
    index_filename = 'weiqi.txt'  # index.txt中每行是'网址 对应的文件名'
    folder = 'weiqi'  # 存放网页的文件夹
    filename = valid_filename(page)  # 将网址变成合法的文件名
    index = open(index_filename, 'a')
    index.write(page.encode('ascii', 'ignore') + '\t' + filename + '\n')
    index.close()
    if not os.path.exists(folder):  # 如果文件夹不存在则新建
        os.mkdir(folder)
    f = open(os.path.join(folder, filename), 'w')
    f.write(content)  # 将网页存入文件
    f.close()





def working():
    global crawled,count,q,max_page,graph
    while count < max_page and q.qsize > 0:
        page = q.get()
        if page not in crawled:
            print page
            #print count
            content=get_page(page)
            if (content == None):
                continue
            #count=count+1
            add_page_to_folder(page, content)
            outlinks = get_all_linksforsports(content, page)
            for link in outlinks:
                #if (q.qsize() + count > max_page):
                    #break
                q.put(link)
            if varLock.acquire():
                print count
                graph[page]=outlinks
                crawled.append(page)
                count=count+1
                varLock.release()


    #q.task_done()


if __name__ == '__main__':
    #seed = sys.argv[1]
    #method = sys.argv[2]
    #max_page = sys.argv[3]
    crawled=[]
    graph={}
    count=0
    max_page=1000
    varLock=threading.Lock()
    #start = time.time()
    start = time.clock()
    q=Queue()
    q.put('http://sports.sina.com.cn/chess/guoxiang/')
    threads=[]
    for i in range(10):
        t = threading.Thread(target=working)
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    #end = time.time()
    end = time.clock()
    print end - start