import httplib2
import os
import random
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

import reddit
import tts
import video

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MISSING_CLIENT_SECRETS_MESSAGE = ""
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
CLIENT_SECRETS_FILE = "client_secrets.json"


def main():
    # script = reddit.get_posts('AskReddit')
    # tts.tts(script)
    # video.create_video()
    # upload_youtube_short("./videos/video.mp4")


def upload_youtube_short(video_file, title="Short Title", description="",
                         keywords="", privacy_status="public"):
    # Check if the file exists
    if not os.path.exists(video_file):
        return "Error: File does not exist."

    # Load client secrets
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))

    # Set up video metadata
    tags = keywords.split(",") if keywords else None
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "27"  # Use category ID for "Shorts" category
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    # Upload the video
    media_body = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media_body)

    # Execute the upload request
    response = resumable_upload(request)

    return response


def resumable_upload(request):
    response = None
    while response is None:
        try:
            status, response = request.next_chunk()
            if response is not None:
                return response
        except HttpError as e:
            raise e


if __name__ == "__main__":
    main()
