import tweepy
import time
import sqlite3
from datetime import date
from textblob import TextBlob
from creds import TWITTER_API_KEY, TWITTER_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

conn = sqlite3.connect('funtech.db')

conn.execute("CREATE TABLE IF NOT EXISTS sentiments (date TEXT, company TEXT, sentiment FLOAT)")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

bugger = 0

companies = ['RBC']

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        global bugger
        "TODO: need to move raw data to db"
        stmt = TextBlob(status.text)
        sent = stmt.sentiment.polarity
        company = ""
        for i in range(len(companies)):
            if companies[i] in status.text:
                company = companies[i]
        bugger +=1
        if(company != ""):
            dat = str(date.today())
            conn.execute("insert into sentiments values (?, ?, ?)", (dat, company, sent))
        if(bugger >= 10):
            conn.commit()
            bugger = 0
        
    def on_error(self, status_code):
        if status_code == 420:
            return False

myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=companies)