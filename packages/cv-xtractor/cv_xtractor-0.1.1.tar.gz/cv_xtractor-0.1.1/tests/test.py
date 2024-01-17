import os
import pytest
from extract import extract_entities_from_file

@pytest.fixture
def pdf_path():
    return os.path.join(os.path.dirname(__file__), '../data/5.pdf')

@pytest.fixture
def skills_file():
    return os.path.join(os.path.dirname(__file__), './jz_skill_patterns.jsonl')

def test_extract_entities_from_file(pdf_path, skills_file):
    # Assuming your sample PDF contains known entities for testing
    expected_entities = {
        'Name': 'Isaac Osei',
        'Phone Number': '0540977343',
        'Email': 'isaacoseianane@gmail.com',
        # 'Locations': ['City1', 'City2'],
        # 'Skills': ['Skill1', 'Skill2'],
        # 'Education': ['University of XYZ', 'College of ABC'],
        # 'Web Links': ['https://www.example.com'],
        # 'Languages Spoken': ['English', 'Spanish'],
        # 'Experience': 'Experience details...',
    }

    # Extract entities from the PDF for testing
    extracted_entities = extract_entities_from_file(pdf_path, skills_file, text_extraction_method='fitz')

    # Check if the extracted entities match the expected ones
    assert extracted_entities == expected_entities

