import os
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer  
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle   
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY       
from reportlab.lib.fonts import addMapping
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas

from src.format_parser import OCROutputParser
from src.utils.helpers import Helpers
from fonts.font_utils import FontUtils

class OCRDocumentGenerator(object):
    def __init__(self, input_filepath):
        self.input_filepath     = input_filepath
        self.ocrOutputParser    = OCROutputParser(input_filepath)

    def get_page_dimensions(self, page):
        _, _, w, h = Helpers.vertices_to_boundingbox(page['page_info']['page_boundingBox']['vertices'])
        return w, h

    def draw_line_text(self, page_canvas, x, y, text, word_space=1.75, horizontal_scale=105, font_name=None, font_size=8):
        txtobj = page_canvas.beginText()
        txtobj.setTextOrigin(x, y)
        txtobj.setWordSpace(word_space)
        txtobj.setHorizScale(horizontal_scale)
        txtobj.setFont(font_name, font_size)
        txtobj.textLine(text=text)
        page_canvas.drawText(txtobj)
        
    def create_pdf(self, pages, pdf_filepath, font_name, font_size=40, scale_factor=4):
        '''
        using first page w & h as canvas
        '''
        w, h                      = self.get_page_dimensions(pages[0])
        pagesize                  = (w/scale_factor, h/scale_factor)
        c                         = canvas.Canvas(pdf_filepath, pagesize=pagesize)
        for page in pages:
            paragraphs, lines     = self.ocrOutputParser.get_page_paragraphs_lines(page)
            
            for line in lines:
                boundingBox, text = line['boundingBox'], line['text']
                x, y, _, _        = boundingBox
                y                 = h - y
                self.draw_line_text(c, x/scale_factor, y/scale_factor, text, 1.75, 105, font_name, font_size/scale_factor)
            c.showPage()
        c.save()

    def generate(self, output_filepath):
        font_name   = 'arial-unicode-ms'
        FontUtils.load_font(font_name)

        pages  = self.ocrOutputParser.get_document_pages()
        self.create_pdf(pages, output_filepath, font_name, 34, 4)
        print('created {} pages PDF at {}'.format(len(pages), output_filepath))