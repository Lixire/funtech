import tweepy
import time
import sqlite3
from textblob import TextBlob
from creds import TWITTER_API_KEY, TWITTER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        "TODO: need to move raw data to db"
        stmt = TextBlob(status.text)
        print(stmt.sentiment.polarity, stmt.sentiment.subjectivity)
    def on_error(self, status_code):
        if status_code == 420:
            return False

myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=['TD Bank'])