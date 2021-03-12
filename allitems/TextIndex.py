#!/usr/bin/env python

INDEX_DIR = "TextIndex.index"

import sys, os, lucene, threading, time
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, LongField, StoredField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

from bs4 import BeautifulSoup
import jieba
import re
import urlparse

"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""


class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'


    def indexDocs(self, root, writer):

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)

        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        count = 0
        filedic = {}
        urlfile = open("sportsinformation.txt", "r")
        for line in urlfile.readlines():
            urlname, pagename, newsdate =line.split('*my_sep*')
            newsdate = newsdate.strip('\n')
            if len(newsdate)==0:
                continue
            filedic[pagename] = [urlname, newsdate]
            '''pageANDurl = line.split('\t')
            urlname = pageANDurl[0]
            webpage = pageANDurl[1].strip('\n')
            filedic[webpage] = urlname'''
        urlfile.close()

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:

                if (filename.endswith('apk') or filename.endswith('pdf') \
                        or filename.endswith('exe') or filename.endswith('rar') \
                        or filename.endswith('zip')):
                    print filename, " SKIP THIS FILE!"
                    continue
                count += 1
                print "adding", filename, " ", count
                try:
                    path = os.path.join(root, filename)
                    file = open(path)
                    contents = unicode(file.read(), 'utf8', 'ignore')
                    soup = BeautifulSoup(contents, "html.parser")
                    title = soup.find("title")
                    if title:
                        title = title.text
                    else:
                        title = "This page has no title"
                    contents = ''.join(soup.findAll(text=True))
                    contents = ' '.join(jieba.cut(contents))
                    file.close()
                    url = filedic[filename][0]
                    newsdate = str(filedic[filename][1])
                    print type(newsdate)
                    print type(url)
                    doc = Document()
                    doc.add(Field("title", title, t1))
                    doc.add(Field("url", url, t1))
                    doc.add(Field("date", newsdate, t1))

                    sites = []
                    site = urlparse.urlparse(url).netloc
                    siteparts = site.split(".")
                    length = len(siteparts)
                    while(length > 0):
                        length -= 1
                        site = '.'.join(siteparts[length:])
                        sites.append(site)
                    site = ' '.join(sites)
                    doc.add(Field("site", site, t2))

                    if len(contents) > 0:
                        print "yes"
                        doc.add(Field("contents", contents, t2))
                    else:
                        print "warning: no content in %s" % filename
                    writer.addDocument(doc)
                except Exception, e:
                    print "Failed in indexDocs:", e


if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('htmlforsports', "sporttestindex")
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e