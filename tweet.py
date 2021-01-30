import tweepy
import os


def create_api():
  consumer_key = os.getenv("CONSUMER_KEY")
  consumer_secret = os.getenv("CONSUMER_SECRET")
  access_token = os.getenv("ACCESS_TOKEN")
  access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)
  api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

  try:
    api.verify_credentials()
  except Exception as e:
    raise e
  return api


class muskStream(tweepy.StreamListener):
  def __init__(self, api, tweets):
    self.api = api
    self.me = api.me()
    self.tweets = tweets 
  def on_status(self, status):
    if status.user.id_str != '44196397':
      return
    else:
      print('append musk tweet')
      self.tweets.put(status.text)
