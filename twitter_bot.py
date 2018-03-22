from time import sleep
from twitter_bot_class import Twitter_Bot

"""Twitter Bot that tweets images, follows users, and retweets"""

consumer_key = '************************'
consumer_secret = '*******************************************'
access_token = '**************************************'
access_token_secret = '******************************************'

bot = Twitter_Bot(consumer_key, consumer_secret, access_token, access_token_secret)
bot.tweet_images()
sleep(20)
bot.follow_user('#realestateinvestor', 3)
sleep(20)
bot.retweet_post('#realestate', 2)
