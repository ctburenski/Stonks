import os
import asyncio
import queue
from dotenv import load_dotenv
from discord.ext import commands
import tweepy

import stock
from tweet import create_api

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
token = os.getenv('DISCORD_BOT_SECRET')


bot = commands.Bot(
    command_prefix="$",
)
bot.author_id = 413829234637799425 # my discord id

api = create_api()
musk_tweets = queue.Queue()
ch_reg = set()


async def read_tweets():
    if not musk_tweets.empty():
        print('read tweet')
        tweet = musk_tweets.get()
        for ch in ch_reg:
            await ch.send(f"From Elon:\n{tweet}")


class muskStream(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
    def on_status(self, status):
        if status.user.id_str != '44196397':
            return
        else:
            print('append musk tweet')
            musk_tweets.put(status.text)


musk_noauth = muskStream(api)
musk_stream = tweepy.Stream(auth=api.auth, listener=musk_noauth)
musk_stream.filter(follow=['44196397'], is_async=True)
print("twitter stream established")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to discord!")


@bot.command(name='get')
async def gme(ctx):
    if len(ctx.message.content.split(' ')) > 1:
        sym = ctx.message.content.split(' ')[1]
        await ctx.send(f"lemme get the price for {sym}...")
        try:
            value = stock.price(ctx.message.content.split(' ')[1])
            await ctx.send(f"${str(value)} USD")
        except stock.NoValue:
            await ctx.send(f"I couldn't find a price for {sym}")
            pass


@bot.command(name='musk')
async def musk(ctx):
    if ctx.channel in ch_reg:
        ch_reg.discard(ctx.channel)
        print("channel added")
        await ctx.send("I won't be posting any more Elon tweets here.")
        return
    else:
        ch_reg.add(ctx.channel)
        print("channel removed")
        await ctx.send("I'll start sending Elon tweets here.")
    while True:
        await read_tweets()
        await asyncio.sleep(7)


bot.run(token)
