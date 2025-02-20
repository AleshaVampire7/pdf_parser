import pytest

from src.extractors.text_extractor.key_value_extractor import KeyValueExtractor

@pytest.fixture
def expected_key_values():
    expectedKeyNames = ["PN:", "LOCATION:", "DESCRIPTION:", "RECEIVER#:", "EXP DATE:", "CERT SOURCE:", "REC.DATE:", "BATCH# : ", "REMARK:", "TAGGED BY:", "SN:", "CONDITION:", "UOM:", "PO:", "MFG:", "DOM:", "LOT# :", "NOTES:", "Qty:"]
    return KeyValueExtractor("data/reference/reference.pdf").extract_key_value_pairs(expectedKeyNames)

@pytest.fixture
def expected_header():
    return "GRIFFON AVIATION SERVICES LLC"

@pytest.fixture
def reference_pdf():
    return KeyValueExtractor("data/reference/reference.pdf")

@pytest.fixture
def test_pdf():
    pdf_path = "data/test_samples/test_sample.pdf"
    return KeyValueExtractor(pdf_path)

def test_key_text_styles(expected_key_values, reference_pdf, test_pdf):
    """
    Iterates over key name coordinates and compares font and size between the reference and test PDFs.
    """
    keyValueCoordinates = reference_pdf.extract_key_value_coordinates(expected_key_values)

    print("\n🔍 DEBUG: Extracted Key-Value Coordinates & Text Styles")

    for key, data in keyValueCoordinates.items():
        coordinates = data["keyCoordinates"]
        page_number = coordinates["page"]

        # Extract text from the given coordinates
        extracted_text = test_pdf.extract_text_from_block(
            page_number, coordinates["x0"], coordinates["y0"], coordinates["x1"], coordinates["y1"]
        ).strip()

        # Extract font and size
        font_size_data = test_pdf.extract_font_and_size_by_coordinates(
            page_number, coordinates["x0"], coordinates["y0"], coordinates["x1"], coordinates["y1"]
        )

        # Debug output
        print(f"📌 Key: {key} → Text: '{extracted_text}' → Font: {font_size_data['font']}, Size: {font_size_data['size']}")

        # Ensure extracted text contains key (to handle minor OCR issues)
        assert key in extracted_text, f"❌ Key mismatch: Expected '{key}' to be inside '{extracted_text}'"

        # Compare font and size with reference PDF
        reference_font_size_data = reference_pdf.extract_font_and_size_by_coordinates(
            page_number, coordinates["x0"], coordinates["y0"], coordinates["x1"], coordinates["y1"]
        )

        assert font_size_data["font"] == reference_font_size_data["font"], f"❌ Font mismatch for '{key}': Expected '{reference_font_size_data['font']}', got '{font_size_data['font']}'"
        assert font_size_data["size"] == reference_font_size_data["size"], f"❌ Size mismatch for '{key}': Expected {reference_font_size_data['size']}, got {font_size_data['size']}"