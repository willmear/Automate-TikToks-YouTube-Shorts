from dotenv import load_dotenv
import assemblyai as aai
import os
from termcolor import colored
from moviepy import *


load_dotenv('.env')
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')
FILE_URL = './speech/speech.mp3'

def transcribe():
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    if transcript.status == aai.TranscriptStatus.error:
        print(colored(transcript.error))
    else:
        print(colored("transcribed"))
        words = transcript.words
        cutVideo(words[-1].end)

def cutVideo(length):
