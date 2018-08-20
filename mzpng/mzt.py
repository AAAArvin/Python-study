# -*- coding:utf-8 -*-
import requests
import urllib.request
from bs4 import BeautifulSoup

Id = 1
html = requests.get('http://tieba.baidu.com/p/2166231880').text
soup = BeautifulSoup(html, 'html.parser')

#抓取图片地址
#抓取img标签且class为BDE_Image的所有内容
img_src=soup.findAll("img",{'class':'BDE_Image'})
for img in img_src:
    img=img.get('src')   #抓取src
    file = open(r'C:\Users\mrsong\PycharmProjects\mzpng\mzt\meizi'+str(Id)+'.png', 'wb')
    file.write(urllib.request.urlopen(img).read())
    print('Downloading...'+str(Id))
    Id = Id + 1
print('succeed!')