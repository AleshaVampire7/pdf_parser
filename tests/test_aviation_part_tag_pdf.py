import pytest
from src.parser import PDFParser

@pytest.fixture
def sample_pdf():
    return "data/test_task.pdf"  # Укажите реальный путь к тестовому PDF

def test_extract_text(sample_pdf):
    parser = PDFParser(sample_pdf)
    text = parser.extract_text()
    assert isinstance(text, str)
    assert len(text) > 0  # Проверяем, что текст не пустой

def test_extract_metadata(sample_pdf):
    parser = PDFParser(sample_pdf)
    metadata = parser.extract_metadata()
    assert isinstance(metadata, dict)
    assert "title" in metadata or "producer" in metadata  # Проверяем ключи

def test_extract_table_data(sample_pdf):
    parser = PDFParser(sample_pdf)
    tables = parser.extract_table_data()
    assert isinstance(tables, list)