from time import sleep
from twitter_bot_class import Twitter_Bot
import os, datetime, glob
import tweepy as tp

"""Posts to twitter with status updates"""

consumer_key = '*************'
consumer_secret = '*************************************************'
access_token = '******************************************'
access_token_secret = '************************************'

bot = Twitter_Bot(consumer_key, consumer_secret, access_token, access_token_secret)
bot.follow_user('#realestate', 2)

#make directory for twitter content if it does not exist
directory = 'twitter_content'
if not os.path.exists(directory):
    os.mkdir(directory)

#change directory
os.chdir(directory)

#get text from file
"""with open('twitter_posts.txt', 'r') as f:
    text_posts = f.readlines()

for l in text_posts:
    if l != '\n':
        try:
            print(l)
            api.update_status(l)
        except tp.TweepError as e:
            print(e.reason)

        sleep(3)
"""
#retweet posts
"""tweets = tp.Cursor(api.search, q='#RealEstate').items(2)

for t in tweets:
    try:
        print(t.text)
        t.retweet()
        sleep(10)
    except tp.TweepError as e:
        print(e.reason)
"""
#follow users
"""tweets = tp.Cursor(api.search, q='#realestateinvestor').items(5)

for t in tweets:
    try:
        print(t.text)
        t.user.follow()
        sleep(10)
    except tp.TweepError as e:
        print(e.reason)
    
"""

