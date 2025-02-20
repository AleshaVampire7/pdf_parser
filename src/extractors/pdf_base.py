import pdfplumber
import fitz
import logging
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from typing import Dict, List, Optional, Union

class PDFBase:

    def __init__(self, file_path: str):
        self.file_path = file_path
        try:
            self.doc = fitz.open(file_path)
        except Exception as e:
            logging.error(f"Ошибка при открытии PDF: {e}")
            raise ValueError("Не удалось открыть PDF-файл")

    def get_metadata(self) -> Dict[str, Optional[str]]:
        return self.doc.metadata if self.doc else {}

    def get_page_count(self) -> int:
        return len(self.doc) if self.doc else 0

    def get_page_size(self) -> List[Dict[str, float]]:
        return [{"page": i + 1, "width": p.rect.width, "height": p.rect.height} for i, p in enumerate(self.doc)]