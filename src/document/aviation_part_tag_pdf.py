from run import PhraseCoordinates
from src.pdf_base import PDFBase
import re

class AviationPartTagPDF(PDFBase):
    """Класс для обработки авиационных PDF-документов"""

    def __init__(self, file_path: str, fields=None):
        """Принимает PDF и список полей, которые нужно извлекать"""
        super().__init__(file_path)
        self.fields = fields or ["PN", "LOCATION", "DESCRIPTION", "RECEIVER#", "EXP DATE", "CERT SOURCE", "REC.DATE", "BATCH# ", "REMARK", "TAGGED BY", "SN", "CONDITION", "UOM", "PO", "MFG", "DOM", "LOT# ", "NOTES", "Qty"]
        self.raw_text = " ".join(self.text_by_lines)
        self.parsed_data = self.parse_text(self.raw_text, self.fields)

    def parse_key_value_from_text(text, keyName):
        """
        Извлекает значение для search_phrase из текста.


        :param text: Текст, который нужно разобрать.
        :param search_phrase: Ключ, который нужно найти (например, "LOT#:").
        :return: Кортеж (ключ, значение) или None, если ключ не найден.
        """
        lines = text.split("\n")  # Разделяем текст на строки
        key = keyName.strip().strip(":")  # Убираем двоеточие и лишние пробелы
        value = []  # Список для хранения значения


        # Флаг, указывающий, что мы нашли search_phrase
        found_search_phrase = False


        for line in lines:
            # Если строка начинается с search_phrase
            if line.startswith(keyName):
                found_search_phrase = True
                # Извлекаем значение после search_phrase
                value.append(line[len(keyName):].strip())
            elif found_search_phrase:
                # Если строка не начинается с search_phrase, но мы уже нашли search_phrase,
                # добавляем её к значению (например, многострочные NOTES)
                if ":" in line:
                    # Если встречается новый ключ, прерываем сбор значения
                    break
                value.append(line.strip())


        # Если search_phrase найден, возвращаем ключ и значение
        if found_search_phrase:
            return key, "\n".join(value).strip()
        else:
            return None
        
    def extract_value_coordinates(full_phrase_coords, key_coords):
        """
        Extracts the coordinates of the value based on the key and full phrase coordinates.
        """
        x0_value = key_coords.x1  # Value starts right after the key
        y0_value = full_phrase_coords.y0  # Same y0 as the full phrase
        x1_value = full_phrase_coords.x1  # Ends at full phrase x1
        y1_value = full_phrase_coords.y1  # Same y1 as the full phrase

        return PhraseCoordinates(full_phrase_coords.page_number, x0_value, y0_value, x1_value, y1_value)
    
    def extract_key_value_coordinates(pdf_path, key_value_dict):
        """
        Extracts key-value coordinates from the PDF and returns them in the desired dictionary format.
        """
        result_dict = {}

        for key, value in key_value_dict.items():
            # 1. Find the full phrase coordinates (key: value)
            formatted_phrase = f"{key}: {value}".strip()
            full_phrase_coords_list = get_phrase_coordinates(pdf_path, formatted_phrase)

            if not full_phrase_coords_list:
                print(f'Фраза "{formatted_phrase}" не найдена')
                continue  # Skip if the full phrase is not found

            full_phrase_coords = full_phrase_coords_list[0]  # Take the first match

            # 2. Find the key coordinates (key:)
            key_coords_list = get_phrase_coordinates(pdf_path, f"{key}:".strip())
            if not key_coords_list:
                print(f'Ключ "{key}:" не найден')
                continue  # Skip if the key is not found

            key_coords = key_coords_list[0]  # Take the first match

            # 3. Calculate the value coordinates
            value_coords = extract_value_coordinates(full_phrase_coords, key_coords)

            # 4. Add to the result dictionary
            result_dict[key] = {
                "value": value,
                "keyCoordinates": {
                    "page_number": key_coords.page_number,
                    "x0": key_coords.x0,
                    "y0": key_coords.y0,
                    "x1": key_coords.x1,
                    "y1": key_coords.y1,
                },
                "valueCoordinates": {
                    "page_number": value_coords.page_number,
                    "x0": value_coords.x0,
                    "y0": value_coords.y0,
                    "x1": value_coords.x1,
                    "y1": value_coords.y1,
                }
            }

        return result_dict