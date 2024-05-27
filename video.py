from dotenv import load_dotenv
import assemblyai as aai

from moviepy.video.fx.crop import crop
from termcolor import colored
from moviepy.editor import *

load_dotenv('.env')
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

FILE_URL = './speech/speech.mp3'


def create_video():
    words = transcribe()
    gameplay = cut_video(words[-1].end)
    gameplay = add_audio(gameplay)
    gameplay = subtitle(gameplay, words)
    gameplay.write_videofile('./videos/video.mp4', codec='libx264', audio_codec='aac', bitrate="5000k")


def transcribe():
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    if transcript.status == aai.TranscriptStatus.error:
        print(colored(transcript.error))
    else:
        print(colored("transcribed", 'green'))
        return transcript.words


def cut_video(length: int):
    gameplay = VideoFileClip("Gameplay.mp4")
    gameplay = gameplay.without_audio()

    (w, h) = gameplay.size
    cropped_clip = crop(gameplay, width=600, height=5000, x_center=w / 2, y_center=h / 2)

    return cropped_clip.set_start(t=0).set_end(t=(length / 1000) + 2)


def add_audio(gameplay: VideoFileClip):
    audio_clip = AudioFileClip(FILE_URL)
    new_audio_clip = CompositeAudioClip([audio_clip])
    gameplay.audio = new_audio_clip
    return gameplay


def subtitle(gameplay: VideoFileClip, words):
    clip_list = [gameplay]

    objects = three_per_line(words)

    for word_group in objects:

        text = ' '.join(word.text for word in word_group)
        print(colored(text, "blue"))

        duration = word_group[-1].end - word_group[0].start

        txt_clip = (TextClip(text, fontsize=60, color='white', font='TheBoldFont',
                             size=(gameplay.w, gameplay.h), method="caption",
                             stroke_width=2, stroke_color="black")
                    .set_position(('center', 'center'))
                    .set_duration(duration / 1000)
                    .set_start(t=word_group[0].start / 1000))

        clip_list.append(txt_clip)

    final_clip = CompositeVideoClip(clip_list)
    return final_clip


def three_per_line(words):
    for i in range(0, len(words), 3):
        yield words[i:i + 3]
