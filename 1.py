# -*- coding:UTF-8 -*-
#!/usr/bin/python3


import requests
import threading
from bs4 import BeautifulSoup
import re


class NetWorkSetting:
    def __init__(self):
        self.proxy = {
            "http": 'http://10.144.1.10:8080',
            "https": 'https://10.144.1.10:8080'}
        self.base_url = 'http://skydocs.int.net.nokia.com/Open%20BGW*Open%20BGW%20Cloud'
        self.naviUrl = 'http://10.133.141.219:8080/informationbrowser/nav/'
        self.contentUrl = 'http://10.133.141.219:8080/informationbrowser/'
        self.myHeaders = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Referer': 'http://www.meizitu.com'
}

setting = NetWorkSetting()
"""
Description    : 将网页图片保存本地
@param imgUrl  : 待保存图片URL
@param imgName : 待保存图片名称
@return 无
"""
def saveImage( imgUrl,imgName ="default.jpg" ):
    response = requests.get(imgUrl, headers=setting.myHeaders, proxies=setting.proxy)
    #response = requests.get(imgUrl, stream=True, headers=setting.myHeaders, proxies=setting.proxy)
    image = response.content
    DstDir="D:\\persion\\picture\\downimg\\"
    print("保存文件"+DstDir+imgName+"\n")
    try:
        with open(DstDir+imgName,"wb") as jpg:
            jpg.write( image)
        return
    except IOError:
        print("IO Error\n")
        return
    finally:
        jpg.close

"""
Description    : 开启多线程执行下载任务
@param filelist:待下载图片URL列表
@return 无
"""

def downImageViaMutiThread( filelist ):
    print "2, enter downImageViaMutiThread"
    task_threads=[]  #存储线程
    count=1
    for file in filelist:
        print file
        filename = file.replace("/","-")
        if 'com-' in filename:
            p = re.compile(r'com-')
        print(filename)
        filename = p.split(filename)[1]
        t = threading.Thread(target=saveImage,args=(file,filename))
        count = count+1
        task_threads.append(t)
    for task in task_threads:
        task.start()
    for task in task_threads:
        task.join()

"""
Description    : 获取图片地址
@param pageUrl : 网页URL
@return : 图片地址列表
"""

def getfilelist(pageUrl):
    print "1, enter getfilelist"
    web = requests.get(pageUrl, headers=setting.myHeaders, proxies=setting.proxy)
    soup = BeautifulSoup(web.text)
    filelist=[]
    #   for photo in soup.find_all('img',{'class':'scrollLoading'}):
    for photo in soup.find_all('img'):
        print photo.get('src')
        filelist.append(photo.get('src'))
    #        filelist.append(photo.get('data-original'))
    print "1, leave getfilelist"
    return filelist

def getweblist(webUrl):
    #http://www.meizitu.com/a/list_1_3.html
    print "===================0, enter getweblist==================="
    weblist=[]
    index = 0
    target_url = webUrl
    while index < 10:
        if index != 0:
            target_url = webUrl + "a/list_1_" + str(index) + ".html"

        print "===================for different page==================="
        print target_url
        web = requests.get(target_url, headers=setting.myHeaders, proxies=setting.proxy)
        if web.status_code == 200:
            soup = BeautifulSoup(web.text)
            for pagelist in soup.find_all('div',{'class':'metaRight'}):
                for link in pagelist.find_all('a'):
                    if link not in weblist:
                        weblist.append(link.get('href'))

            for pagelist in soup.find_all('div',{'class':'pic'}):
                for link in pagelist.find_all('a'):
                    print link.get('href')
                    if link not in weblist:
                        weblist.append(link.get('href'))
        else:
            print "open page error!!!"
        index += 1
    print "0, leave getweblist"


    f = open("test.txt",'w+')
    for item in weblist:
        print "===================for item in weblist==================="
        print item
        f.write(item)
        f.write('\n')
    f.close()
    return weblist

if __name__ == "__main__":
    webUrl = 'http://www.meizitu.com/'
    list = getweblist(webUrl)
    print "===================page================"
    for page in list:
        imagelist = getfilelist(page)
        downImageViaMutiThread(imagelist)

    print "===================the end================"