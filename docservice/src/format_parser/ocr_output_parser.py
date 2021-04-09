import os
import io
import json
from src.utils.helpers import Helpers

class OCROutputParser(object):
    def __init__(self, filename):
        self.filename   = filename

    def get_page_paragraphs_lines(self, page):
        page_paragraphs    = []
        page_lines         = []
        
        if 'regions'in page.keys():
            for para_region in page['regions']:
                if 'class' in para_region.keys() and 'regions' in para_region.keys():
                    if para_region['class'] == 'PARA':
                        lines = []
                        for line_region in para_region['regions']:
                            if 'class' in line_region.keys() and 'regions' in line_region.keys():
                                if line_region['class'] == 'LINE':
                                    words = []
                                    for word_region in line_region['regions']:
                                        if 'class' in word_region.keys() and 'text' in word_region.keys():
                                            if word_region['class'] == 'WORD':
                                                words.append(word_region['text'])

                                    lines.append(' '.join(words) + '\n')
                                    page_lines.append({'boundingBox': Helpers.vertices_to_boundingbox(line_region['boundingBox']['vertices']), 
                                                'text': ' '.join(words)})

                        page_paragraphs.append({'boundingBox': Helpers.vertices_to_boundingbox(para_region['boundingBox']['vertices']), 
                                                'text': ''.join(lines)})
        return page_paragraphs, page_lines

    def get_document_name(self):
        with io.open(self.filename, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        return data['data'][0]['file_name']

    def get_document_locale(self):
        with io.open(self.filename, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        return data['data'][0]['file_locale']

    def get_document_pages(self):
        with io.open(self.filename, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        return data['data']