import fitz
import pdfplumber
import logging
import numpy as np
from pyzbar.pyzbar import decode
from typing import Dict, List, Optional, Union

from src.extractors.pdf_base import PDFBase


class PDFTextExtractor(PDFBase):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.file_path = file_path

    def extract_text(self) -> Optional[str]:
        try:
            with pdfplumber.open(self.file_path) as pdf:
                return "\n".join([page.extract_text() or "" for page in pdf.pages]).strip()
        except Exception as e:
            logging.error(f"Ошибка при чтении текста: {e}")
            return None

    def get_phrase_coordinates(self, phrase: str) -> List[Dict]:
        coordinates = []
        words_list = phrase.split()
        for page_num, page in enumerate(self.doc):
            words = page.get_text("words")
            for i in range(len(words) - len(words_list) + 1):
                if [w[4].lower() for w in words[i:i+len(words_list)]] == [w.lower() for w in words_list]:
                    x0 = min(w[0] for w in words[i:i+len(words_list)])
                    y0 = min(w[1] for w in words[i:i+len(words_list)])
                    x1 = max(w[2] for w in words[i:i+len(words_list)])
                    y1 = max(w[3] for w in words[i:i+len(words_list)])
                    coordinates.append({"page": page_num + 1, "x0": x0, "y0": y0, "x1": x1, "y1": y1})
        return coordinates
    
    def extract_text_from_block(self, page_number, x0, y0, x1, y1):
       """
       Extracts text from a specific block in the PDF.
       """
       doc = fitz.open(self.file_path)
       page = doc[page_number - 1]
       rect = fitz.Rect(x0, y0, x1, y1)
       text = page.get_textbox(rect)
       return text
    
    def extract_font_and_size_by_coordinates(self, page_number, x0, y0, x1, y1, expand=3):
        doc = fitz.open(self.file_path)
        page = doc[page_number - 1]


        text_data = page.get_text("dict")


        extracted_text = self.extract_text_from_block(page_number, x0, y0, x1, y1,)
        x0 -= expand
        y0 -= expand
        x1 += expand
        y1 += expand


        for block in text_data["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        tx, ty = span["bbox"][0], span["bbox"][1]
                        bx, by = span["bbox"][2], span["bbox"][3]
                        span_text = span["text"].strip()


                        is_in_box = (x0 <= tx <= x1 and y0 <= ty <= y1) or (x0 <= bx <= x1 and y0 <= by <= y1)


                        if is_in_box and span_text in extracted_text:
                            return {"font": span["font"], "size": span["size"]}


        return {"font": None, "size": None}
