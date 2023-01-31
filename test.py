import requests
import urllib.request


video_data = requests.get('https://www.reddit.com/r/aww/comments/10n45t5/just_wow/').json()
print(video_data)
"""
url = video_data[0]["data"]["children"][0]["data"]["secure_media"]["reddit_video"][
"fallback_url"
]
print("checking")
urllib.request.urlretrieve(url,filename="video.mp4",)
"""