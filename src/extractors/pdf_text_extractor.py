import pdfplumber
import logging
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from typing import Dict, List, Optional, Union


class PDFTextExtractor(PDFBase):
    """Класс для работы с текстом в PDF"""

    def extract_text_by_lines(self) -> Optional[List[str]]:
        """Извлекает текст построчно"""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                return [page.extract_text() or "" for page in pdf.pages]
        except Exception as e:
            logging.error(f"Ошибка при чтении текста: {e}")
            return None

    def get_phrase_coordinates(self, phrase: str) -> List[Dict]:
        """Находит координаты фразы в PDF"""
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