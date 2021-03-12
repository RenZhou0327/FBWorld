# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import time
import codecs

f=open('sinaglbaindex.txt','r')
urlall={}
for line in f.xreadlines():
    ls = line.split()
    # print ls[0],ls[1]
    urlall[ls[1]] = ls[0]
f.close()


def getimage(u):
    global crawled
    global count
    file = codecs.open('/media/EE/lab4/samples4/testfolder/sinaglba/'+u,'r')
    content=file.read()
    file.close()
    soup = BeautifulSoup(content, "html.parser")
    for img in soup.find_all('img'):
        src=img.get('src','')
        if(not src or not src.endswith('jpg')):
            continue
        if(src.startswith('http')==False):
            src='http:'+src
        if(src not in crawled):
            crawled.append(src)
        else:
            continue
        alt=img.get('alt','')
        if(not alt):
            continue
        url=urlall[u]
        get=url+'*my_sep*'+alt+'*my_sep*'+src
        save = codecs.open('sinaglbaimg.txt', 'a')
        save.write(get.encode('utf-8', 'ignore'))
        save.write('\n')
        save.close()
        count=count+1
        print count
count=0
crawled=[]
start=time.clock()
for u in urlall:
    getimage(u)
end=time.clock()
print end-start