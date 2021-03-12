# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import time
import jieba
import codecs

f=open('sinadombaindex.txt','r')
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
    src=""
    if(src==""):
        for img in soup.find_all('span',{'class':'date'}):
            src=img.string
            src=src.strip()
            src=src[0:4]+src[5:7]+src[8:10]
    if(src.isdigit()==True):
        url=urlall[u]
        get=url+'*my_sep*'+u+'*my_sep*'+src
        save = codecs.open('sinaglbainf.txt', 'a')
        save.write(get.encode('utf-8', 'ignore'))
        save.write('\n')
        save.close()
        count = count + 1
        print count


count=0
crawled=[]
start=time.clock()
print(urlall)
for u in urlall:
    getimage(u)
end=time.clock()
print end-start