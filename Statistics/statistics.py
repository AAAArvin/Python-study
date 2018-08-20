#--*--coding:utf-8--*--
"""
@author:mrsong
"""
import string
import io
import re
import pandas as pd


#读取文本文件
path = r'C:\Users\mrsong\PycharmProjects\Statistics\The Last Leaf.txt'

#转换所有英文字母为小写
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()
wordlist = re.split('[\n\r "",.-?!-]', text.lower())
data = pd.Series(wordlist)
print(data.value_counts())