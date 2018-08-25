#--*--coding:utf-8--*--
"""
@author: mrsong
"""

from MyQR import myqr

class QrCode(object):
    #生成普通二维码
    def NormalCode(self):
        myqr.run(words = 'https://three-year-old.github.io/', save_name = 'normalqrcode.png', save_dir = r'C:\Users\mrsong\PycharmProjects\个性二维码\QrCode')

    #生成带图片的艺术二维码
    def PicCode(self):
        picture = 'Source/erdou.png'
        myqr.run(words = 'https://three-year-old.github.io/', picture = picture, colorized=True, save_name = 'picqrcode.png', save_dir = r'C:\Users\mrsong\PycharmProjects\个性二维码\QrCode')

    #生成动态二维码
    def GifCode(self):
        picture = 'Source/cat.gif'
        myqr.run(words = 'https://three-year-old.github.io/', picture = picture, colorized = True, save_name = 'gifqrcode.gif', save_dir = r'C:\Users\mrsong\PycharmProjects\个性二维码\QrCode')

if __name__ == '__main__':
    qrCode = QrCode()
    qrCode.NormalCode()
    qrCode.PicCode()
    qrCode.GifCode()