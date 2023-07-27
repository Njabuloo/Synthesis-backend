import re
import json
from typing import List
from PyPDF2 import PdfReader
from openai_api import openai_api
from share_point_api import Sharepoint
import firebase_admin
from firebase_admin import auth, db,credentials
from dotenv import load_dotenv
import os


def extract_text(file_name: str) -> str:
    """
    Extract text from a PDF file.

    args:
        file_name (str): The name of the PDF file from which text needs to be extracted.

    Returns:
        str: The extracted text from the PDF.

    Raises:
        Exception: If the specified PDF file is not found or cannot be opened.

    """
    try:
        # Open the PDF file
        with open(file_name, "rb") as f:
            # Create a PdfReader object to read the PDF file
            file = PdfReader(f)
            # Extract the text from each page of the PDF and concatenate them
            text: str = "".join(page.extract_text() for page in file.pages)
            # close file
            f.close()
    except (FileNotFoundError, IOError):
        # Handle the case when the file is not found or cannot be opened
        raise Exception(f"File {file_name} not found or cannot be opened.")
    # Return the extracted text from the PDF
    return text


def redact_personal_information(text: str) -> str:
    """
    Redacts personal information from a string using regex.

    Args:
        text (str): The input string containing personal information to be redacted.

    Returns:
        str: The modified string with redacted personal information.

    """
    # Define the regex patterns to match email addresses and phone numbers
    regex_patterns = [
        re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+"),
        re.compile(r"(\+27[\s]?)?\d{2,3}[\s-]?\d{3}[\s-]?\d{4}"),
    ]
    # Iterate over the regex patterns and replace matches with "REDACTED"
    for pattern in regex_patterns:
        text: str = pattern.sub("", text)
    # Return the modified text with redacted personal information
    return text


def clean_str(original_text: str) -> dict:
    """
    Clean and convert a string to a JSON-formatted string.

    Args:
        original_text (str): The input string that needs to be cleaned and converted.

    Returns:
        str: A JSON-formatted string containing the cleaned text.

    """
    # Clean the original_text by removing newline characters ('\n')
    cleaned_text: str = original_text.replace("\n", "")
    # Convert the cleaned_text to a JSON-formatted string using json.dumps()
    json_string: dict = json.loads(cleaned_text)
    # Return the JSON-formatted string
    return json_string


def extract_entities(text: str) -> dict:
    """Extracts skills, technologies, programming languages and any relevant information that can be found in a resume.

    Args:
        text (str): The text to extract entities from.

    Returns:
        dict: A dictionary containing the extracted entities.
    """
    response = openai_api(text)
    content = response.choices[0].message.content
    return clean_str(content)

def add_to_db(data: json, file) -> None:
    """
    Add data to the Firebase Realtime Database.

    Parameters:
        data (json): A JSON object containing the data to be added to the database.

    Returns:
        None
    """

    # Initialize Firebase Admin SDK with service account credentials
    cred = credentials.Certificate("./cv-chomper-firebase-adminsdk-fdrf1-b789536d7e.json")
    if not firebase_admin._apps:
        url = {
            "databaseURL": 'https://cv-chomper-default-rtdb.firebaseio.com/'
        }
        firebase_admin.initialize_app(cred, url)

    # Get a reference to the 'resumes_data' collection in the database
    ref = db.reference('/')
    candidates_ref = ref.child('resumes_data')

    # Create a new unique key for the candidate and set the data at that location
    new_candidate = candidates_ref.push()
    data['url'] = file
    new_candidate.set(data)
    print(data)


def process_resumes_data(username: str, password: str, url: str) -> None:
    """
    Process resumes data by extracting text, redacting personal information,
    and extracting entities before adding them to the database.

    args:
        username (str): The username to authenticate with Sharepoint.
        password (str): The password to authenticate with Sharepoint.
        url (str): The URL of the Sharepoint site containing the resumes.

    Returns:
        None
    """
    resumes = Sharepoint(username, password, url)
    [file_names, files_urls] = resumes.get_files()
    file_paths: List[str] = resumes.download_files(file_names)
    for file, url in zip(file_paths, files_urls):
        text: str = extract_text(file)
        text: str = redact_personal_information(text)
        entities: dict = extract_entities(text)
        updated_url = 'https://synthesissoftware.sharepoint.com' + url
        add_to_db(entities, updated_url)
 


if __name__ == "__main__":
    load_dotenv()

    # Get values of environment variables and assign them to respective variables
    username: str = os.environ["USERNAME"]
    password: str = os.environ["USER_PASSWORD"]
    sharepoint_url: str = os.environ["SHAREPOINT_URL"]
    
    process_resumes_data(username, password, sharepoint_url)
    