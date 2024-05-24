from pathlib import Path

import openai
from openai import OpenAI
from termcolor import colored
import os
from dotenv import load_dotenv
import assemblyai as aai

load_dotenv('.env')

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
)
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
FILE_URL = './speech/speech.mp3'


def tts():
    speech_file_path = Path(__file__).parent / "speech" / "speech.mp3"
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input="Today is a wonderful day to build something people love!"
        )

        response.stream_to_file(speech_file_path)
    except openai.APIConnectionError as e:
        # Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.APIError as e:
        print(f"OpenAI Error: {e}")
        pass
    except openai.RateLimitError as e:
        # Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass


