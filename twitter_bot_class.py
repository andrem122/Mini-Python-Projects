from time import sleep
import tweepy as tp
import os

class Twitter_Bot:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.api = self.authenticate()

    #apply twitter credentials to get api
    def authenticate(self):
        auth = tp.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return tp.API(auth)

    def loop_through_tweets(self, query, num_items, action):
        tweets = tp.Cursor(self.api.search, q=query).items(num_items)

        for t in tweets:
            try:
                print(t.text)
                if action is 'follow':
                    getattr(getattr(t, 'user'), action)()
                else:
                    getattr(t, action)()
                sleep(10)
            except tp.TweepError as e:
                print(e.reason)

    #retweet posts by search query
    def retweet_post(self, query, num_items):
        self.loop_through_tweets(query=query, num_items=num_items, action='retweet')

    #follow users by search query
    def follow_user(self, query, num_items):
        self.loop_through_tweets(query=query, num_items=num_items, action='follow')

    #update status with scraped web images
    def tweet_images(self):
        #go to the directory with the images
        os.chdir('twitter_content/twitter_images')

        #get images in  current directory
        images = os.listdir('.')

        #tweet each image
        for image in images:
            try:
                self.api.update_with_media(image)
                sleep(10)
            except tp.TweepError as e:
                print(e.reason)
