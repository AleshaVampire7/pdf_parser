import pytest
from src.extractors.pdf_image_extractor import PDFImageExtractor

@pytest.fixture
def reference_pdf():
    return PDFImageExtractor("data/reference/reference.pdf")

@pytest.fixture
def test_pdf():
    return PDFImageExtractor("data/test_samples/test_sample.pdf")

def test_barcode_count(reference_pdf, test_pdf):
    ref_barcodes = reference_pdf.extract_barcodes()
    test_barcodes = test_pdf.extract_barcodes()
    assert len(ref_barcodes) == len(test_barcodes), "❌ Number of barcodes does not match!"

def test_barcode_values(reference_pdf, test_pdf):
    ref_barcodes = reference_pdf.extract_barcodes()
    test_barcodes = test_pdf.extract_barcodes()

    for ref, test in zip(ref_barcodes, test_barcodes):
        assert isinstance(ref["barcode"], str), f"❌ Barcode should be a string, got {type(ref['barcode'])}"
        assert isinstance(ref["type"], str), f"❌ Barcode type should be a string, got {type(ref['type'])}"
        assert ref["barcode"] == test["barcode"], f"❌ Barcode mismatch on page {ref['page']}"
        assert ref["type"] == test["type"], f"❌ Barcode type mismatch on page {ref['page']}"

def test_barcode_positions(reference_pdf, test_pdf):
    ref_barcodes = reference_pdf.extract_barcodes()
    test_barcodes = test_pdf.extract_barcodes()

    for ref, test in zip(ref_barcodes, test_barcodes):
        assert isinstance(ref["position"], dict), "❌ Position should be a dictionary"
        assert set(ref["position"].keys()) == {"x", "y", "width", "height"}, "❌ Position keys mismatch"

        for key in ["x", "y", "width", "height"]:
            assert isinstance(ref["position"][key], (int, float)), f"❌ {key} should be a number, got {type(ref['position'][key])}"