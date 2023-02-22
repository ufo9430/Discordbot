import discord
from discord.ext import commands
from discord.ext import tasks

import praw
from RedDownloader import RedDownloader

import os
import urllib.request
import datetime
from time import sleep
import openai_cli

import re


SUB_REDDIT = 'memes'
LIMIT = 30


CHANNEL_ID = int(open("channel.txt").readline())
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
        while True:
            random_post = r.subreddit(SUB_REDDIT).random()
            if(random_post.score < 500):
                continue
            if(random_post.over_18):
                await ch.send("it is too dangerous for kid")
            url = random_post.url
            video_url = 'https://www.reddit.com'+random_post.permalink
            title = random_post.title
            parsedTitle = re.sub(r"[^a-zA-Z]", "", title)
            if parsedTitle == "": parsedTitle = "file"
            print(url)
            if (url[8] == 'i'):
                urllib.request.urlretrieve(url, "%s.gif" %(parsedTitle))
                image = discord.File("%s.gif" %(parsedTitle), filename="image.gif")
                await ch.send(title)
                await ch.send(file=image)
                os.remove("%s.gif" %(parsedTitle))
                break
            elif (url[8] == 'v'):
                RedDownloader.Download(video_url, output=parsedTitle, quality = 360)
                sleep(0.5)
                video = discord.File("%s.mp4" %(parsedTitle), filename = "vid.mp4")
                await ch.send(title)
                await ch.send(file=video)
                os.remove("%s.mp4" %(parsedTitle))
                break
    except Exception as error:
        print(error)
        await ch.send('error')

@app.event
async def on_ready():
    print('Ready')
    dailyRedditPost.start()
    await app.change_presence(status=discord.Status.online, activity=None)

# 명령어 파트

@app.command()
async def helpme(ctx):
    ch = app.get_channel(CHANNEL_ID)
    print("test")
    embed = discord.Embed(
    title = 'dlsgusalsssi',
    description = 'Reddit 포스트 스크래핑, gpt 챗봇 외 개발중'
    )
    embed.add_field(name="Reddit 기능 설명", value="/subreddit : 서브레딧 설정, 기본값=/memes\n/limit : 인기 포스트 개수 제한, 기본값 10\n/meme : 포스트 올림",inline=False)
    embed.add_field(name="GPT 챗", value="Hyeonmin과의 챗\n/chat 내용 : 대화",inline=False)
    embed.add_field(name="AI 그림",value="키워드 기반 그림 그려주는 AI\n/draw 내용 : 그림",inline=False)
    await ch.send(embed=embed)

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
    if int(text)>=1 and int(text)<=100:
        LIMIT = int(text)
        await ch.send("Limit is modified to %d" % LIMIT)
    else:
        await ch.send("Limit can be changed to 1~100")

@app.command()
async def meme(ctx):
    await postMemes()
#챗봇
@app.command()
async def chat(ctx, *input):
    ch = app.get_channel(CHANNEL_ID)
    input_str = ' '.join(input)
    await ch.send("%s" %(openai_cli.chat(input_str, openai_cli.history_first)))

@app.command()
async def draw(ctx, *input):
    ch = app.get_channel(CHANNEL_ID)
    input_str = ' '.join(input)
    response_url = openai_cli.draw(input_str)
    urllib.request.urlretrieve(response_url, "image.jpg")
    image = discord.File("image.jpg", filename="image.jpg")
    await ch.send(file=image)
    os.remove("image.jpg")
"""
@app.command()
async def dungeon(ctx):
    ch = app.get_channel(CHANNEL_ID)
    await ch.send("데모")
    await ch.send("/act 명령")
    await ch.send(openai_cli.RPGinit())

@app.command()
async def act(ctxj, *input):
    ch = app.get_channel(CHANNEL_ID)
    input_str = ' '.join(input)
    await ch.send("%s" %(openai_cli.RPG(input_str,openai_cli.history_RPG)))

"""
#loop
@tasks.loop(seconds=1)
async def dailyRedditPost():
    now = datetime.datetime.now()
    if now.hour == 0 and now.minute == 0 and now.second == 0:
        await postMemes()

app.run(token)


"""
        hot_posts = r.subreddit(SUB_REDDIT).hot(limit=LIMIT)
        for posts in hot_posts:
            if(posts.over_18):
                await ch.send("it is too dangerous for kid")
            url = posts.url
            video_url = 'https://www.reddit.com'+posts.permalink
            title = posts.title
            parsedTitle = re.sub(r"[^a-zA-Z]", "", title)
            if parsedTitle == "": parsedTitle = "file"
            print(url)
            if (url[8] == 'i'):
                urllib.request.urlretrieve(url, "%s.gif" %(parsedTitle))
                image = discord.File("%s.gif" %(parsedTitle), filename="image.gif")
                await ch.send(title)
                await ch.send(file=image)
                os.remove("%s.gif" %(parsedTitle))
                break
            elif (url[8] == 'v'):
                RedDownloader.Download(video_url, output=parsedTitle, quality = 360)
                sleep(0.5)
                video = discord.File("%s.mp4" %(parsedTitle), filename = "vid.mp4")
                await ch.send(title)
                await ch.send(file=video)
                os.remove("%s.mp4" %(parsedTitle))
                break
"""
