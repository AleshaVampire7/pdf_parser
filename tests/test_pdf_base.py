import pytest

from src.extractors.pdf_base import PDFBase

@pytest.fixture
def reference_pdf():
    """Возвращает объект PDFBase для эталонного PDF."""
    return PDFBase("data/reference/reference.pdf")

@pytest.fixture
def test_pdf():
    """Возвращает объект PDFBase для тестируемого PDF."""
    return PDFBase("data/test_samples/test_sample.pdf")

def test_pdf_opening(reference_pdf):
    """Проверяет, открывается ли PDF без ошибок."""
    assert reference_pdf.doc is not None

def test_page_count(reference_pdf, test_pdf):
    """Сравнивает количество страниц эталонного и тестируемого PDF."""
    assert reference_pdf.get_page_count() == test_pdf.get_page_count(), "Количество страниц не совпадает"

def test_metadata(reference_pdf, test_pdf):
    """Сравнивает метаданные PDF."""
    ref_metadata = reference_pdf.get_metadata()
    test_metadata = test_pdf.get_metadata()

    # Проверяем только ключи, которые существуют в обоих файлах
    common_keys = set(ref_metadata.keys()) & set(test_metadata.keys())

    for key in common_keys:
        assert ref_metadata[key] == test_metadata[key], f"Метаданные не совпадают для ключа {key}"

def test_page_sizes(reference_pdf, test_pdf):
    """Сравнивает размеры страниц эталонного и тестируемого PDF."""
    ref_sizes = reference_pdf.get_page_size()
    test_sizes = test_pdf.get_page_size()

    assert len(ref_sizes) == len(test_sizes), "Количество страниц не совпадает"

    for ref, test in zip(ref_sizes, test_sizes):
        assert ref["width"] == pytest.approx(test["width"], rel=0.01), f"Ширина страницы {ref['page']} не совпадает"
        assert ref["height"] == pytest.approx(test["height"], rel=0.01), f"Высота страницы {ref['page']} не совпадает"