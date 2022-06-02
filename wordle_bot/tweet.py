import tweepy
import json

with open('credentials.json') as fh:
    creds = json.load(fh)

client = tweepy.Client(
    consumer_key=creds['consumer_key'],
    consumer_secret=creds['consumer_secret'],
    access_token=creds['access_key'],
    access_token_secret=creds['access_secret']
)

client.create_tweet(text='This is a test')