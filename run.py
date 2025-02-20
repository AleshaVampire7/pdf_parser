from src.extractors.text_extractor.key_value_extractor import KeyValueExtractor

keyValueExtractor = KeyValueExtractor('data/test_samples/test_sample.pdf')

key_names = ["PN:", "LOCATION:", "DESCRIPTION:", "RECEIVER#:", "EXP DATE:", "CERT SOURCE:", "REC.DATE:", "BATCH# : ", "REMARK:", "TAGGED BY:", "SN:", "CONDITION:", "UOM:", "PO:", "MFG:", "DOM:", "LOT# :", "NOTES:", "Qty:"]


keyValues = keyValueExtractor.extract_key_value_pairs(key_names) 

print(keyValues)

keyValueWithCoordinates = keyValueExtractor.extract_key_value_coordinates(keyValues)

print(keyValueWithCoordinates)