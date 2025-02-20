from src.extractors.text_extractor.utils.pdf_text_extractor import PDFTextExtractor
from src.extractors.utils.phrase_coordinates import PhraseCoordinates

class KeyValueExtractor(PDFTextExtractor):

    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.pdf_path = file_path
    
    def parse_key_value_from_text(self, text, keyName):
       lines = text.split("\n")
       key = keyName.strip().strip(":")
       value = []

       found_search_phrase = False

       for line in lines:
           if line.startswith(keyName):
               found_search_phrase = True
               value.append(line[len(keyName):].strip())
           elif found_search_phrase:
               if ":" in line:
                   break
               value.append(line.strip())

       if found_search_phrase:
           return key, "\n".join(value).strip()
       else:
           return None
   
    def extract_value_coordinates(self, full_phrase_coords, key_coords):
        x0_value = key_coords["x1"]
        y0_value = full_phrase_coords["y0"]
        x1_value = full_phrase_coords["x1"]
        y1_value = full_phrase_coords["y1"]

        return PhraseCoordinates(full_phrase_coords["page"], x0_value, y0_value, x1_value, y1_value)
    
    def extract_key_value_pairs(self, key_names):
        key_value_dict = {}

        for key in key_names:
            coordinates = self.get_phrase_coordinates(key)
            
            pdf_sizes = self.get_page_size()
            fileWidth = pdf_sizes[0]["width"]

            for coords in coordinates:
                extracted_text = super().extract_text_from_block(
                    coords["page"],
                    coords["x0"],
                    coords["y0"],
                    fileWidth,
                    coords["y1"] + 50
                )

                result = self.parse_key_value_from_text(extracted_text, key)
                if result:
                    key_found, value = result
                    key_value_dict[key_found] = value

        return key_value_dict


    def extract_key_value_coordinates(self, key_value_dict):
        result_dict = {}

        for key, value in key_value_dict.items():
            formatted_phrase = f"{key}: {value}".strip()
            full_phrase_coords_list = super().get_phrase_coordinates(formatted_phrase)

            if not full_phrase_coords_list:
                print(f'Фраза "{formatted_phrase}" не найдена')
                continue

            full_phrase_coords = full_phrase_coords_list[0]

            key_coords_list = super().get_phrase_coordinates(f"{key}:".strip())
            if not key_coords_list:
                print(f'Ключ "{key}:" не найден')
                continue

            key_coords = key_coords_list[0]

            value_coords = self.extract_value_coordinates(full_phrase_coords, key_coords)

            result_dict[key] = {
                "value": value,
                "keyCoordinates": {
                    "page": key_coords["page"],
                    "x0": key_coords["x0"],
                    "y0": key_coords["y0"],
                    "x1": key_coords["x1"],
                    "y1": key_coords["y1"],
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