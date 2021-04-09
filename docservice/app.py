import os
from src.document_generator import OCRDocumentGenerator

input_filepath  = '/Users/kd/Workspace/python/document-formatting/docservice/data/ocredv15.json'
output_filepath = '/Users/kd/Workspace/python/document-formatting/docservice/data/ocredv15.json.pdf'

OCRPDFDocument  = OCRDocumentGenerator(input_filepath)
OCRPDFDocument.generate(output_filepath)