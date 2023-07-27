import os
import openai
from dotenv import load_dotenv

def openai_api(text:str) -> dict:
    """
    Function to interact with the OpenAI GPT-3.5-turbo API and generate chat completions.

    Parameters:
        text (str): The user's input text or prompt for the chat completion.

    Returns:
        dict: A dictionary representing the response obtained from the OpenAI API.
    """
    
    # Load environment variables from the .env file in the current directory
    load_dotenv()
    
    # Set the OpenAI API key from the environment variable
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Create a chat completion request to the GPT-3.5-turbo model
    response: dict = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You will be provided a text, extract entities into the following bins, education,work experience, skills, \
                    and certification. The skills include technologies and programming languages. All the bins must be there on the python dictionary object that you return."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        temperature=0.5,
        max_tokens=4097
    )

    # Return the response from the OpenAI API
    return response
