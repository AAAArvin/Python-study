#--*--coding:utf-8--*--
"""
@author: mrsong
"""

import os

string = input('请输入: ')
#打开文件
with open(r'C:\Users\mrsong\PycharmProjects\敏感词覆盖\filtered_words.txt', 'rt') as f:
    words = f.read()
f.close()
wordlists = words.split(" ")
for word in wordlists:
    if(word in string):
        s = ''
        for letter in word:
            s += s + '*'
        string = string.replace(word, s)
print(string)