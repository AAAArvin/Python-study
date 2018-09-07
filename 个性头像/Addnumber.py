#--*--coding:utf-8--*--
"""
@author: mrsong
"""

from PIL import Image, ImageDraw, ImageFont
import random


class Individuation(object):
    def Addnum(self):
        #打开图片
        im = Image.open('./images/Dog.png')
        #设置随机生成的数字
        randomNum = str(random.randint(1, 99))
        #图片大小
        width, height = im.size
        #设置数字显示的位置
        width_new = width * 0.6
        height_new = height * 0.1
        #设置数字字体
        font = ImageFont.truetype('arial.ttf',36)
        draw = ImageDraw.Draw(im)
        draw.text((width_new, height_new), randomNum, font = font, fill = (255, 33, 33))
        im.save('./images/Dog_done.png')

if __name__ == '__main__':
    individuation = Individuation()
    individuation.Addnum()
