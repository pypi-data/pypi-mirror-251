from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='cv_xtractor',
    version='0.1.1',
    description='A Python package for extracting information from CVs (resumes).',
    long_description=Path("README.md").read_text(),
    long_description_content_type='text/markdown',
    author='Odai Israel Ago',
    author_email='agocoded@gmail.com',
    url='https://github.com/remotown/CV-XTRACTOR',
    packages=find_packages(exclude=['tests', 'data']),
    include_package_data=True,
    install_requires=[
        'spacy',
        'pdfplumber',
        'python-docx',
        'PyMuPDF',
    ],
    package_data={'cv_xtractor': ['jz_skill_patterns.jsonl']},
)
