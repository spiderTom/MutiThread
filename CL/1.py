# -*- coding:UTF-8 -*-
#!/usr/bin/python3


import requests
import threading
from bs4 import BeautifulSoup
import re


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.158.100.9:8080',
            "https": 'https://10.158.100.9:8080'}
        self.base_url = 'http://t66y.com/thread0806.php?fid=20&search=digest'
        self.prifixUrl = 'http://t66y.com/'
        self.contentUrl = 'http://t66y.com/thread0806.php?fid=20'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://t66y.com'
}


isProxyNeeded = True
setting = NetWorkSetting()
session = requests.Session()
targetUrlList = []


def getUrlList(homeurl):
    if isProxyNeeded:
        result = session.get(homeurl, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(homeurl, headers=setting.myHeaders)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content)
        for link in soup.find_all(title="打開新窗口"):
            # and link.get('href') not in targetUrlList
            if link.get('href').find("htm_data/") != -1:
                temp = setting.prifixUrl + link.get('href')
                print "======================="
                print temp
                print "======================="
                targetUrlList.append(temp)


def getUrlPage(page, pageindex):
    if isProxyNeeded:
        result = session.get(page, headers=setting.myHeaders, proxies=setting.proxy)
    else:
        result = session.get(page, headers=setting.myHeaders)
    if result.status_code == 200:
        f = open("D:\\jike\\CL\\" + str(pageindex) + ".html", 'w+')
        f.write(result.content)
        f.close()


def downPageViaMutiThread(filelist):
    task_threads = []  #存储线程
    count = 1
    for page in targetUrlList:
        t = threading.Thread(target=getUrlPage,args=(page, str(count)))
        count += 1
        task_threads.append(t)
    for task in task_threads:
        task.start()
    for task in task_threads:
        task.join()


print "before getUrlList"
getUrlList(setting.base_url)
print "after getUrlList"
downPageViaMutiThread(targetUrlList)


print "it is the end"
