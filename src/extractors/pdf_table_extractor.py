import pdfplumber
import fitz
import logging
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from typing import Dict, List, Optional, Union

class PDFTableExtractor(PDFBase):
    """Класс для работы с таблицами в PDF"""

    def extract_tables(self) -> Optional[List[List[str]]]:
        """Извлекает таблицы"""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                tables = [page.extract_table() for page in pdf.pages if page.extract_table()]
            return tables if tables else None
        except Exception as e:
            logging.error(f"Ошибка при извлечении таблиц: {e}")
            return None