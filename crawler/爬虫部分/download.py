# -*- coding:utf-8 -*-
import urllib
from Queue import Queue
import threading
from bs4 import BeautifulSoup
import urllib2
import re
import urlparse
import os
import time
import sys
f=open('/media/EE/lab4/samples4/testfolder/sinadombaimg.txt','r')
urlall=[]
for line in f.xreadlines():
    ls = line.split("*my_sep*")
    # print ls[0],ls[1]
    urlall.append(ls[2])
f.close()

count=0

def get_image(url,stuNum):
    global count
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request,timeout=2.0)
        img_name = str(stuNum+1)+".jpg"
        filename = "/media/EE/lab4/samples4/testfolder/dombapic/" + img_name
        with open(filename, "wb") as f:
            f.write(response.read())  # 将内容写入图片
            count=count+1
            print(count)
        return filename
    except:
        print('访问空')

stuNum =-1
url = ''
for i in range(1687):
    stuNum = stuNum+1
    get_image(urlall[stuNum],stuNum)