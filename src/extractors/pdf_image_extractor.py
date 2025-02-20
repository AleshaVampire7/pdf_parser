import pdfplumber
import fitz
import logging
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from typing import Dict, List, Optional, Union

class PDFImageExtractor(PDFBase):
    """Класс для работы с изображениями и штрих-кодами"""

    def extract_images(self) -> Optional[List[Dict[str, Union[int, str]]]]:
        """Извлекает изображения из PDF"""
        images = []
        for page_num, page in enumerate(self.doc):
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = self.doc.extract_image(xref)
                images.append({
                    "page": page_num + 1,
                    "image_index": img_index,
                    "width": base_image["width"],
                    "height": base_image["height"],
                    "image_format": base_image["ext"]
                })
        return images if images else None

    def extract_barcodes(self) -> List[Dict]:
        """Извлекает штрих-коды"""
        barcodes = []
        with pdfplumber.open(self.file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                img = page.to_image().original  # PIL image
                cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)  # OpenCV image
                decoded_objects = decode(cv_image)

                for obj in decoded_objects:
                    barcode_info = {
                        "page": page_num + 1,
                        "barcode": obj.data.decode("utf-8"),
                        "type": obj.type,
                        "position": {"x": obj.rect.left, "y": obj.rect.top, "width": obj.rect.width, "height": obj.rect.height}
                    }
                    barcodes.append(barcode_info)

        return barcodes