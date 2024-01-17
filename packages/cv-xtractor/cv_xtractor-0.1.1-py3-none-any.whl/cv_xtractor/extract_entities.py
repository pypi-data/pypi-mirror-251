import os
import json
import re
import spacy
import pdfplumber
import fitz
from docx import Document
from spacy.matcher import Matcher

# Load spaCy models
nlp = spacy.load("en_core_web_sm")


def pdf_to_text_fitz(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".pdf":
        return extract_text_with_fitz(file_path)
    elif file_extension.lower() == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return ""
    
def pdf_to_text_plumber(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension.lower() == ".pdf":
        return extract_text_with_plumber(file_path)
    elif file_extension.lower() == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return ""


def extract_text_with_fitz(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text = text + str(page.get_text())
    tx = " ".join(text.split("/n"))
    return tx

def extract_text_with_plumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


# Function to extract and format names
def extract_name(resume_text):
    lines = [line.strip() for line in resume_text.split('\n') if line.strip()]
    first_10_lines = '\n'.join(lines[:10])

    matcher = Matcher(nlp.vocab)
    # Define name patterns
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]  # First name, Middle name, Middle name, and Last name
        # Add more patterns as needed
    ]
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(first_10_lines)
    matches = matcher(doc)

    formatted_names = []
    for match_id, start, end in matches:
        span = doc[start:end]
        # Format the extracted name with only the first letter of each word capitalized
        formatted_name = ' '.join(word.capitalize() for word in span.text.split())
        formatted_names.append(formatted_name)

        # Filter names based on keywords, numbers, and special characters
        filtered_names = filter_names(formatted_names)

        # Print filtered names as a list
        if len(filtered_names) != 0:
            return(filtered_names[0])
        else:
            # Regex pattern to find a line with "Name:" and capture the text after it
            pattern = re.compile(r'\bName\s*(.*)', re.IGNORECASE)
            
            # Search for the pattern in the text
            match = re.search(pattern, first_10_lines)
            
            # Check if a match is found
            if match:
                # Extract the text after "Name:"
                name_text = match.group(1).strip()
                # Remove special characters using regex
                name_text = re.sub(r'[^a-zA-Z0-9\s]', '', name_text)

                return(name_text)
            else:
                return lines[0]

    return None

# Function to filter names based on keywords, numbers, and special characters
def filter_names(names):
    filtered_names = []
    for name in names:
        # Check if the name contains any of the specified keywords or has numbers/special characters
        keywords_to_exclude = ["curriculum", "vitae", "p.o", "web", "designer", "east", 'legon', 'box', 'it', 'software', 'portfolio',
                              'full', 'developer', 'ghana', 'tech', 'db', 'summary', 'programming', 'ui', 'frontend', 'data', 'accra',
                              'engineer', 'developer', ]
        if not any(keyword.lower() in name.lower() for keyword in keywords_to_exclude) and not any(char.isdigit() for char in name):
            filtered_names.append(name)
    return filtered_names



# Function to filter names based on keywords, numbers, and special characters
def filter_names(names):
    filtered_names = []
    for name in names:
        # Check if the name contains any of the specified keywords or has numbers/special characters
        keywords_to_exclude = ["curriculum", "vitae", "p.o", "web", "designer", "east", 'legon', 'box', 'it', 'software', 'portfolio',
                              'full', 'developer', 'ghana', 'tech', 'db', 'summary', 'programming', 'ui', 'frontend', 'data', 'accra',
                              'engineer', 'developer', ]
        if not any(keyword.lower() in name.lower() for keyword in keywords_to_exclude) and not any(char.isdigit() for char in name):
            filtered_names.append(name)
    return filtered_names


# Function to extract phone number
def extract_mobile_number(text):
    contact_number = None
    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number
        

# Function to extract email
def extract_email(email):
    # Extract email addresses using regular expression
    emails = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", email)

    # If email addresses are found
    if emails:
        # Clean up and standardize the first email address
        cleaned_email = emails[0].lower().strip(';')

        # Remove anything after '.com'
        cleaned_email = cleaned_email.split('.com')[0] + '.com'

        # Remove leading/trailing parentheses
        cleaned_email = cleaned_email.strip('()')

        # Remove leading/trailing hyphens
        cleaned_email = cleaned_email.strip('-')

        # Remove leading/trailing slashes
        cleaned_email = cleaned_email.strip('/')

        # Remove leading/trailing spaces
        cleaned_email = cleaned_email.strip()

        return cleaned_email

    return None


# Function to extract locations
def extract_cities_countries(resume_text):
    lines = resume_text.split('\n')
    first_10_lines = '\n'.join(lines[:10])
    
    # Process the resume text using spaCy
    doc = nlp(first_10_lines)

    # Extract entities with the label "GPE" (Geopolitical Entity)
    geopolitical_entities = [ent.text.strip() for ent in doc.ents if ent.label_ == 'GPE']

    # Filter entities based on your criteria (e.g., check if the entity is a city or country)
    cities_countries = filter_cities_countries(geopolitical_entities)

    return list(set(cities_countries))

def filter_cities_countries(entities):
    # Example: Filter entities to include only cities and countries
    valid_entities = [entity for entity in entities if is_city_or_country(entity)]
    # Check if 'LinkedIn' is in the list and exclude it
    if 'LinkedIn' in valid_entities:
        valid_entities.remove('LinkedIn')
    return valid_entities

def is_city_or_country(entity):
    return len(entity) > 2 and not any(char.isdigit() for char in entity)


# Get the path to the directory containing this script
# script_dir = os.path.dirname(os.path.realpath(__file__))

# Load skills from jz_skill_patterns.jsonl
# skills_file_path = os.path.join(script_dir, 'jz_skill_patterns.jsonl')

def load_skills():
    skills_file_path = os.path.join(os.path.dirname(__file__), 'jz_skill_patterns.jsonl')
    skills = []

    with open(skills_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            skill_data = json.loads(line)
            skills.append(skill_data)

    return skills



# Function to extract skills
def extract_skills(resume_text, skills_data):
    if not skills_data:
        return []

    # Check if "entity_ruler" is already in the pipeline
    if "entity_ruler" not in nlp.pipe_names:
        # Adding "entity_ruler" to the pipeline before "ner" for skills extraction
        ruler = nlp.add_pipe("entity_ruler", before="ner")
        
        # Load patterns from skills_data
        patterns = [{"label": entry["label"], "pattern": entry["pattern"]} for entry in skills_data]
        ruler.add_patterns(patterns)

    # Process the resume text
    doc = nlp(resume_text)

    # Extract skills
    skills = [ent.text for ent in doc.ents if ent.label_ == 'SKILL']

    # Capitalize skills and remove duplicates
    skills = list(set([skill.capitalize() for skill in skills]))
    return skills



# Function to extract education
def extract_education(resume_text):
    doc = nlp(resume_text)

    # Keywords related to educational institutions
    education_keywords = ['college', 'university', 'be', 'b.e.', 'b.e', 'bs', 'b.s', 'me', 'm.e', 'm.e.', 'ms', 'm.s', 
                          'btech', 'b.tech', 'm.tech', 'mtech', 'ssc', 'hsc', 'cbse', 'icse', 'x', 'xii','bsc','phd','msc','mphil']

    # Extract organizations using spaCy's named entity recognition (NER)
    organizations = [ent.text for ent in doc.ents if ent.label_ == "ORG"]

    # Filter organizations based on keywords
    education_organizations = [org for org in organizations if any(keyword.lower() in org.lower() for keyword in education_keywords)]

    # Filter out organizations that don't have "college" or "university"
    education_organizations = [org for org in education_organizations if 'college' in org.lower() or 'university' in org.lower()]

    #2nd Fn
    # Remove empty lines
    education_organizations = [org.strip() for org in education_organizations if org.strip()]

    # Process each organization to remove unwanted words
    processed_organizations = []
    for org in education_organizations:
        # Split the organization into words
        words = org.split()

        # Check if the word before "college" or "university" doesn't start with a capital letter
        for i, word in enumerate(words):
            if word.lower() in ['college', 'university', 'school'] and i > 0 and not words[i - 1].istitle():
                words.pop(i - 1)
                break

        # Join the words back into a string
        processed_organizations.append(' '.join(words))

    return processed_organizations


# Function to extract web links
def extract_web_links(resume_text):
    # Define a regular expression pattern for detecting URLs
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    # Find all matches in the resume text
    links = re.findall(url_pattern, resume_text)

    return links

# Function to extract languages
def extract_languages(resume_text):
    # Define a regular expression pattern for language detection
    language_pattern = re.compile(r'\b(?:English|Spanish|German|Twi|Ga|French|Hausa|Italianozz|Spanish|Inglés)\b', re.IGNORECASE)

    # Find matches using the regular expression pattern
    matches = language_pattern.findall(resume_text)

    return matches



# Function to extract experience
def extract_experience(resume_text):
    # List to store the lines containing the exact keywords
    lines_with_keywords = []
    # List of keywords related to work experience
    experience_keywords = [
    'experience', 'professional experience', 'professional experience', 'industry experience', 'employment history',
    'work experience', 'work experiences', 'work summary', 'professional history', 'employer details', 'summary',
    'technical experience', 'industrial experience', 'experiences', 'personal summary',
    'professional background', 'work history', 'internship experience', 'date position institution duties',
    'professional skills and experience', 'working experience', 'relevant experience', 'past experience',
    'relevant experience', 'working history'
]
    
    # List of refinement keywords related to skills and education
    refinement_keywords = [
        'educations', 'educational details', 'educational profile','education and training','skills and competence',
        'educational qualifications', 'academic qualifications', 'skill', 'skills','training','refree','refrees','interests',
        'volunteer activities','intern', 'technologies',
        'technical skill', 'skill highlights', 'Computer Skills', 'it skills', 'education','achievements','refrences',
        ]


    # Iterate through each line in the resume text
    for line in resume_text.split('\n'):
        # List to store the lines containing the keywords
        lines_with_keywords = []

        # Iterate through each line in the resume text
        for line in resume_text.split('\n'):
            # Check if the line exactly matches any of the specified keywords
            if any(keyword.lower() == line.strip().lower() for keyword in experience_keywords):
                lines_with_keywords.append(line)
    
    # Check if the list is empty
    if not lines_with_keywords:
        # Check if a line starts with the word "project" (capital "P")
        project_line_index = next((i for i, line in enumerate(resume_text.split('\n')) if line.strip().startswith('Project')), None)

        if project_line_index is not None:
            # Include the project line and all text after it
            lines_after_project = resume_text.split('\n')[project_line_index+1:]
            result = f"Project\n" + '\n'.join(lines_after_project)
            return result
        else:
            return "No experience keyword found."
    else:
        # Grab the first keyword
        first_keyword = lines_with_keywords[0]

        # Extract all text after the first keyword
        text_after_keyword = extract_text_after_keyword(resume_text, first_keyword)

        # Include the first keyword at the top
        result = f"{first_keyword}\n{text_after_keyword}"

    # Refine the extracted text
    refined_result = refine_extracted_text(result, refinement_keywords)

    # Check if the refined keyword is not None
    if refined_result is not None:
        # Split the result into lines and check if the refined keyword is at the beginning of any line
        lines = result.strip().split('\n')
        refined_lines = [line.strip() for line in lines if line.strip().lower().startswith(refined_result.lower())]

        if refined_lines:
            # Grab all text before the refined keyword (considering the first occurrence)
            index = result.lower().find(refined_lines[0].lower())
            text_before_refined_keyword = result[:index].strip()
            # print(text_before_refined_keyword)
            return text_before_refined_keyword
        else:
            # print(refined_result)
            return refined_result
    else:
        return "No refined keyword found."


def extract_text_after_keyword(resume_text, keyword):
    # Find the index of the keyword in the resume text
    index = resume_text.lower().find(keyword.lower())

    # If the keyword is found, extract all text after the keyword
    if index != -1:
        return resume_text[index + len(keyword):].strip()
    else:
        return None

def refine_extracted_text(text_after_keyword, refinement_keywords):
    # List to store refined keywords found in the text
    refined_keywords = []

    # Iterate through each refinement keyword
    for keyword in refinement_keywords:
        # Find the index of the keyword in the text
        index = text_after_keyword.lower().find(keyword.lower())

        # Check if the keyword is found
        if index != -1:
            # Check if the keyword is the only word on the line
            lines = text_after_keyword.split('\n')
            for i, line in enumerate(lines):
                if keyword.lower() in line.lower() and line.strip().lower() == keyword.lower():
                    # Add the keyword and the line number to the refined list
                    refined_keywords.append((keyword, i + 1))
                    break

    # Sort the refined keywords based on the line number
    refined_keywords.sort(key=lambda x: x[1])

    # Get the first refined keyword
    if refined_keywords:
        first_refined_keyword = refined_keywords[0][0]
        return first_refined_keyword
    else:
        return text_after_keyword





# Function to extract entities from a PDF
def extract_entities_from_file(pdf_path):
    # Extract text from PDF
    text = pdf_to_text_fitz(pdf_path)
    textP = pdf_to_text_plumber(pdf_path)

    # Extract entities
    name = extract_name(textP)
    phone_number = extract_mobile_number(text)
    email = extract_email(text) 
    locations = extract_cities_countries(text)

    # Use the load_skills() function wherever you need to access the skills data
    skills_data = load_skills()
    skills = extract_skills(text, skills_data)

    education = extract_education(text)
    web_links = extract_web_links(text)
    languages = extract_languages(text)
    experience = extract_experience(text)

    # Return extracted entities as a dictionary
    extracted_entities = {
        'Name': name,
        'Phone Number': phone_number, 
        'Email': email,
        'Locations': locations,
        'Skills': skills, 
        'Education': education, 
        'Web Links': web_links,
        'Languages Spoken': languages,
        'Experience': experience,
    }

    return extracted_entities



