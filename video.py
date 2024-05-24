from dotenv import load_dotenv
import assemblyai as aai
import os

from moviepy.audio.AudioClip import CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.fx.crop import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from termcolor import colored
from moviepy import *
from moviepy.editor import *

load_dotenv('.env')
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

FILE_URL = './speech/speech.mp3'


def create_video():
    words = transcribe()
    gameplay = cut_video(words[-1].end)
    gameplay = add_audio(gameplay)
    subtitle(gameplay)
    gameplay.write_videofile('./videos/video.mp4', codec='libx264', audio_codec='aac', bitrate="5000k")


def transcribe():
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    if transcript.status == aai.TranscriptStatus.error:
        print(colored(transcript.error))
    else:
        print(colored("transcribed"))
        return transcript.words


def cut_video(length: int):
    gameplay = VideoFileClip("Gameplay.mp4")
    gameplay = gameplay.without_audio()

    (w, h) = gameplay.size
    cropped_clip = crop(gameplay, width=600, height=5000, x_center=w/2, y_center=h/2)

    return cropped_clip.set_start(t=0).set_end(t=(length / 1000) + 2)


def add_audio(gameplay: VideoFileClip):
    audio_clip = AudioFileClip(FILE_URL)
    new_audio_clip = CompositeAudioClip([audio_clip])
    gameplay.audio = new_audio_clip
    return gameplay


def subtitle(gameplay: VideoFileClip):
    pass
