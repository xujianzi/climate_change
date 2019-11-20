__author__ = "Jian"

## Make sure install modules below before running code
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json

from textblob import TextBlob

import twitter_credentials

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import re

import io
import sys
import datetime
import time
import os
from pathlib import Path

## Unmark the code below if you can't display the text
#sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

# # # # TWITTER CLIENT # # # # 
class TwitterClient():
    def __init__(self, twitter_user=None):
        # twitter_user can be twitter user id or motif(keywords)
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth, wait_on_rate_limit= True, wait_on_rate_limit_notify= True)
        self.twitter_user = twitter_user
        
    def get_twitter_client_api(self):
        return self.twitter_client
    
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            print ('...%s tweets have been downloaded so far' % len(tweets))
        return tweets
        
    def get_user_timeline_tweets_bytime(self, num_tweets, young_id = None, old_id = None):
        # Extract tweets older than or younger than a a specific id
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user, since_id= young_id, max_id = old_id).items(num_tweets):
            tweets.append(tweet)
            print ('...%s tweets have been downloaded so far' % len(tweets))
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id = self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id = self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets
    
    def get_search_tweets(self, num_tweets = 200, old_id= None, young_id = None):
        # Function to extract tweets about specific motif from time A to time B
        # num_tweets: the tweets number you want to extract
        # old_id: extracting tweets more older than the id of one specific tweet
        # young_id: extracting tweets more recent than the id of a tweet
        obj_tweets = []       
        for tweet in Cursor(self.twitter_client.search, q = self.twitter_user, 
        since_id = young_id, max_id = old_id).items():
            obj_tweets.append(tweet)
            print ('...%s tweets have been downloaded so far...' % len(obj_tweets))
            if len(obj_tweets) >= num_tweets:
                break
        return obj_tweets

        # # Functionality that get rid of retweets
        # tweets = self.twitter_client.search(self.twitter_user, count = 100)
        # all_the_tweets = []
        # for tweet in tweets:
        #     if 'RT @' not in tweet.text:
        #         all_the_tweets.append(tweet)
        # oldest_tweet = all_the_tweets[-1].id - 1
        # while len(tweets) != 0:
        #     tweets = self.twitter_client.search(self.twitter_user, count = 100,max_id = oldest_tweet)
        #     for tweet in tweets:
        #         if 'RT @' not in tweet.text:
        #             all_the_tweets.append(tweet)
        #     print ('...%s tweets have been downloaded so far...' % len(all_the_tweets))
        #     oldest_tweet = all_the_tweets[-1].id - 1
        #     if len(all_the_tweets) >= num_tweets:
        #         break
        # return all_the_tweets

    def get_search_tweets_byid(self, num_tweets = 200, old_id= None, young_id = None):
        # Extract tweets older than or younger than a a specific id
        tweets = []
        try:
            for tweet in Cursor(self.twitter_client.search, q = self.twitter_user, 
            since_id= young_id, max_id = old_id).items(num_tweets):
                tweets.append(tweet)
                print ('...%s tweets have been downloaded so far' % len(tweets))
        except BaseException as e:
            print('Error on data; %s', str(e))
            with open('temp.txt', 'a') as f:
                for tweet in tweets:
                    js_temp = json.dumps(tweet._json)
                    f.write(js_temp)
                    f.write('\n')

        return tweets
        
    def get_search_tweets_bytime(self):
        search_tweets = []
        oldest_date = datetime.datetime.utcnow() - datetime.timedelta(hours = 12)
        print(oldest_date)
        for tweet in Cursor(self.twitter_client.search, q = self.twitter_user, until = oldest_date).items():
            #if 'RT @' not in tweet.text:
            search_tweets.append(tweet)
            print('...%s tweets have been downloaded so far' % len(search_tweets))
            print('tweet created at ',tweet.created_at)
        return search_tweets

    def limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                time.sleep(15*60)
                continue
            except StopIteration:
                break

# # # # TWITTER AUNTHENTICATER # # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

# # # # TWITTER STREAMMER # # # #
class TwitterStreamer():
    '''
    Class for streaming and processing tweets
    '''
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()

    def stream_tweets(self, fetched_tweets_filename, tag_list):
        
        #This handles Twitter authentication and the connection ot the Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.auth
        stream = Stream(auth, listener)

        stream.filter(track=tag_list)

# # # # TWITTER LISTENER # # # #
class TwitterListener(StreamListener):
    '''
    This is basic listener class that just prints received tweets to stdout
    '''
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print('Error on data; %s', str(e))
        return True
    
    def on_error(self, status):
        if status == 420:
            #returing False in on_data method in case rate limits occurs
            return False
        print(status)

# # # # TWEET ANALYSIS # # # # 
class TweetAnalyzer():
    '''
    Functionality for analyzing and categorizing content from tweets
    '''
    def clean_tweet(self, tweet):
        '''
        data cleaning
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    
    def analyze_sentiment(self, tweet):
        '''
        simple sentiment analysis: 1 represents positive attitude; 0 for neutral; -1 for nagative 
        '''
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        '''
        transform the tweets data to the clean pandas dataframe
        '''
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        
        df['user'] = np.array([tweet.user.name for tweet in tweets])
        df['corordinate'] = np.array([tweet.coordinates for tweet in tweets])
        df['place'] = np.array([tweet.place for tweet in tweets])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        #df['city'] = np.array([tweet.place.name for tweet in tweets])
        #df['country'] = np.array([tweet.place.country for tweet in tweets])
        return df

    def tweets_to_data_frame_new(self, tweets):
        df = pd.DataFrame(data=[tweet['text'] for tweet in tweets], columns=['tweets'])
        
        df['user'] = np.array([tweet['user']['name']  for tweet in tweets])
        #df['location'] = np.array([tweet['user']['location']  for tweet in tweets])
        df['place'] = np.array([tweet['place'] for tweet in tweets])
        df['id'] = np.array([tweet['id'] for tweet in tweets])
        df['len'] = np.array([len(tweet['text']) for tweet in tweets])
        df['date'] = np.array([tweet['created_at'] for tweet in tweets])
        df['likes'] = np.array([tweet['favorite_count'] for tweet in tweets])
        df['retweets'] = np.array([tweet['retweet_count'] for tweet in tweets])
        df['city'] = np.array([tweet['place']['name'] if tweet['place'] != None else None for tweet in tweets])
        return df

    def stream_to_data_frame(self, filepath):
        '''
        file needs to be jason format, this function is for converting downloaded json format
        file to pandas df
        '''
        tweets_data_path = filepath
        tweets_data = []
        tweets_file = open(tweets_data_path, "r")
        for line in tweets_file:
            try:
                tweet = json.loads(line)
                tweets_data.append(tweet)
            except:
                continue
        print('...%s tweets have been downloaded so far...' % len(tweets_data))
        tweets = tweets_data       
        df = self.tweets_to_data_frame_new(tweets)
        return df


class DftoSaveFiles():
    '''
    Functionality for save tweets(dataframe format) to files, df needs to be pandas dataframe obj
    '''
    def __init__(self,filename):
        self.filename = filename

    def df_to_csv(self,folder,df):
        filename = self.filename
        filepath = os.path.join(Path(folder),str(filename)+r'.csv')
        if not os.path.exists(filepath):
            df.to_csv(filepath, mode = 'a', index = False, sep= ',')
            return True
        else:
            print('There is already a exsiting file named '+filename)
        

if __name__ == '__main__':
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()


    