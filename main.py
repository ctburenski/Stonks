import os
import asyncio
import queue
from dotenv import load_dotenv
from discord.ext import commands
import tweepy

from stock import price, NoValue
from tweet import create_api, muskStream

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
token = os.getenv('DISCORD_BOT_SECRET')

if not token:
	print("The bot requires each of the secrets listed in the README to be stored in a .env file.")
	quit()


api = create_api()
musk_tweets = queue.Queue()

musk_noauth = muskStream(api, musk_tweets)
musk_stream = tweepy.Stream(auth=api.auth, listener=musk_noauth)
musk_stream.filter(follow=['44196397'], is_async=True)
print("twitter stream established")


bot = commands.Bot(
  command_prefix="$",
)
bot.author_id = 413829234637799425 # my discord id


@bot.event
async def on_ready():
  print(f"{bot.user.name} has connected to discord!")


@bot.command(name='get')
async def gme(ctx):
  sym = ctx.message.content.split(' ')
  if len(sym) > 1:
    sym = sym[1]
    await ctx.send(f"lemme get the price for {sym}...")
    try:
      value = price(ctx.message.content.split(' ')[1])
      await ctx.send(f"${str(value)} USD")
    except NoValue:
      await ctx.send(f"I couldn't find a price for {sym}")
      pass


async def read_tweets(tweets, channels):
  if not tweets.empty():
    print('read tweet')
    tweet = tweets.get()
    for ch in channels:
      await ch.send(f"From Elon:\n{tweet}")

ch_reg = set()

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
    await read_tweets(musk_tweets, ch_reg)
    await asyncio.sleep(7)


bot.run(token)
