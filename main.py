import tts, video, reddit


def main():
    script = reddit.get_posts('AskReddit')
    tts.tts(script)
    video.create_video()


if __name__ == "__main__":
    main()
