import os, requests, requests.auth

from dotenv import load_dotenv

load_dotenv('.env')
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
API_KEY = os.getenv('REDDIT_API_KEY')
PASSWORD = os.getenv('REDDIT_PASSWORD')
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, API_KEY)
data = {
    'grant_type': 'password',
    'username': os.getenv('REDDIT_USERNAME'),
    'password': os.getenv('REDDIT_PASSWORD'),
}
headers = {"User-Agent": "MyAPI/0.0.1"}


def get_auth():
    print("Getting authorization token...")
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    return response.json()['access_token']


TOKEN = get_auth()
headers["Authorization"] = f'bearer {TOKEN}'


def get_posts(subreddit, limit=1):
    params = {'limit': limit}
    post = requests.get(f'https://oauth.reddit.com/r/{subreddit}/controversial',
                        headers=headers, params=params).json()
    print(post)
    title = post['data']['children'][0]['data']['title']
    post_id = post['data']['children'][0]['data']['id']
    comment_params = {'limit': 3, 'sort': 'top', 'depth': 0}
    comments = requests.get(f'https://oauth.reddit.com/r/{subreddit}/comments/{post_id}',
                            headers=headers, params=comment_params).json()

    comments_list = extract_body_fields(comments)

    return title + ' ' + '. '.join(comment for comment in comments_list)


def extract_body_fields(comment_data):
    body_fields = []

    if isinstance(comment_data, dict):
        for key, value in comment_data.items():
            if key == "body":
                body_fields.append(value)
            else:
                body_fields.extend(extract_body_fields(value))
    elif isinstance(comment_data, list):
        for item in comment_data:
            body_fields.extend(extract_body_fields(item))

    return body_fields
