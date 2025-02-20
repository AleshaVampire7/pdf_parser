import pdfplumber
import logging
import numpy as np
from pyzbar.pyzbar import decode
from typing import Dict, List, Optional, Union

from src.extractors.pdf_base import PDFBase

class PDFTableExtractor(PDFBase):

    def extract_tables(self) -> Optional[List[List[str]]]:
        try:
            with pdfplumber.open(self.file_path) as pdf:
                tables = [page.extract_table() for page in pdf.pages if page.extract_table()]
            return tables if tables else None
        except Exception as e:
            logging.error(f"Ошибка при извлечении таблиц: {e}")
            return None