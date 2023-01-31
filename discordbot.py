import discord
from discord.ext import commands
from discord.ext import tasks

import praw
from RedDownloader import RedDownloader

import os
import urllib.request
import datetime

SUB_REDDIT = 'memes'
LIMIT = 10
CHANNEL_ID = #channel_id
token = open("token.txt",'r').readline()

r = praw.Reddit(client_id="#client_id",
                client_secret="#client_secret",
                user_agent="user_agent",
                )

app = commands.Bot(command_prefix='/', intents=discord.Intents.all())

# 기타 함수 파트
async def postMemes():
    try:
        ch = app.get_channel(CHANNEL_ID)
        hot_posts = r.subreddit(SUB_REDDIT).hot(limit=LIMIT)
        for posts in hot_posts:
            url = posts.url
            video_url = 'https://www.reddit.com'+posts.permalink
            title = posts.title
            if (url[8] == 'i'):
                urllib.request.urlretrieve(url, "meme.gif")
                image = discord.File("meme.gif", filename="image.gif")
                await ch.send(title)
                await ch.send(file=image)
                os.remove("meme.gif")
                break
            elif (url[8] == 'v'):
                RedDownloader.Download(video_url, output="vid")
                video = discord.File("vid.mp4", filename = "vid.mp4")
                await ch.send(title)
                await ch.send(file=video)
                os.remove("vid.mp4")
                break
    except:
        await ch.send('error')
# 명령어 파트

@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=None)


@app.command()
async def subreddit(ctx, text):
    ch = app.get_channel(CHANNEL_ID)
    global SUB_REDDIT
    SUB_REDDIT = text
    await ch.send("Subreddit is changed to "+SUB_REDDIT)


@app.command()
async def limit(ctx, text):
    ch = app.get_channel(CHANNEL_ID)
    global LIMIT
    LIMIT = int(text)
    await ch.send("Limit is modified to %d" % LIMIT)

@app.command()
async def meme(ctx):
    await postMemes()

@tasks.loop(seconds=1)
async def dailyRedditPost(self):
    if  datetime.datetime.now().second == 0 and datetime.datetime.now().minute == 0 and datetime.datetime.now().hour == 0:
        await postMemes()

app.run(token)
