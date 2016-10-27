# -*- coding:UTF-8 -*-
#!/usr/bin/python3


import requests
import threading
from bs4 import BeautifulSoup
import re

"""
Description    : 将网页图片保存本地
@param imgUrl  : 待保存图片URL
@param imgName : 待保存图片名称
@return 无
"""
def saveImage( imgUrl,imgName ="default.jpg" ):
    response = requests.get(imgUrl, stream=True)
    image = response.content
    DstDir="D:\\persion\\picture\\downimg\\"
    print("保存文件"+DstDir+imgName+"\n")
    try:
        with open(DstDir+imgName ,"wb") as jpg:
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
    web = requests.get(pageUrl)
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
    print "0, enter getweblist"
    web = requests.get(webUrl)
    print web.status_code
    soup = BeautifulSoup(web.text)
    weblist=[]
    for pagelist in soup.find_all('div',{'class':'metaRight'}):
        for link in pagelist.find_all('a'):
            weblist.append(link.get('href'))
    print "0, leave getweblist"
    return weblist

if __name__ == "__main__":
    webUrl = 'http://www.meizitu.com/'
    list = getweblist(webUrl)
    for page in list:
        print page
        imagelist=getfilelist(page)
        downImageViaMutiThread(imagelist)