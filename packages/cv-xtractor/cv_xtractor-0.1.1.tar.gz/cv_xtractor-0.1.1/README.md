# CV-Xtractor

CV-Xtractor is a Python package designed for parsing information from CVs (resumes). It leverages spaCy for natural language processing, providing features to extract key details such as names, phone numbers, email addresses, skills, education information, and more.

## Installation

Install CV-Xtractor using pip:

```bash
pip install cv-xtractor
```

Additionally, download the spaCy English language model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

Here's a simple example of how to use CV-Xtractor in your Python code:

```python
from cv_xtractor.extract_entities import extract_entities_from_file

# Replace 'your_cv.pdf' with the path to your CV file
cv_file_path = 'your_cv.pdf'

# Extract entities from the CV
entities = extract_entities_from_file(cv_file_path)

# Print the extracted information
print(entities)
```

This will output a dictionary containing various details extracted from the CV, such as names, contact information, skills, education, and more.

For more advanced usage and customization, please refer to the [documentation]