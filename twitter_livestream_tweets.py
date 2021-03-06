# -*- coding: utf-8 -*-
"""Twitter_LiveStream_Tweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dHFkHAzYdZ1nCGAuANQMchHP8RZteH0K
"""

import tweepy
import configparser
import pandas as pd
import re
import numpy as np

"""##Twitter API Set Up"""

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_secret = config['twitter']['api_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class Streamer(tweepy.Stream):
  
  tweets = []
  limit = 1     #100 for keyword


  def on_status(self, status):
    self.tweets.append(status)
    #print(status.user.screen_name + ': ' + status.text)

    if len(self.tweets) == self.limit:
      self.disconnect()

stream_tweet = Streamer(api_key, api_secret, access_token, access_token_secret)

#Stream by keywords and/or hashtag OR by user

#keywords = ['ADA', '#Cardano']

#stream_tweet.filter(track=keywords)

#Stream by Users
users = ['G_Ramirez95'] #could have multiple or just one
user_ids = []

for user in users:
  user_ids.append(api.get_user(screen_name=user).id)

print(user_ids)

stream_tweet.filter(follow=user_ids)

#Create a Dataframe

columns = ['User', 'Tweet']
data = []

for tweet in stream_tweet.tweets:
  if not tweet.truncated:
    data.append([tweet.user.screen_name, tweet.text])

  else:
    data.append([tweet.user.screen_name, tweet.extended_tweet['full_text']])

df = pd.DataFrame(data, columns=columns)

print(df)