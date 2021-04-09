import os
from reportlab.pdfbase import pdfmetrics      
from reportlab.pdfbase.ttfonts import TTFont   

class FontUtils(object):
    @classmethod
    def load_font(self, font_name='arial-unicode-ms'):
        pdfmetrics.registerFont(TTFont(font_name, os.path.join(os.getcwd(), 'fonts', font_name + '.ttf')))