import twitter_processing
from twitter_processing import TweetAnalyzer
import json
import os
from pathlib import Path


def main():
    '''
    save the tweets data as jason format.
    '''
    folder = Path(dir_name)
    filepath = os.path.join(folder,filename)
    twitter_client = twitter_processing.TwitterClient(motif)
    temp_tweets = twitter_client.get_search_tweets(num_tweets = num_tweets, young_id=1177019422516662273)
    with open(filepath, 'a') as f:
        for tweet in temp_tweets:
            js = json.dumps(tweet._json)
            f.write(js)
            f.write('\n')
    #p = os.path.join(folder,str(news)+ r'.csv')

def users_extract():
    pass
    

if __name__ == "__main__":
    motif = "trump"
    num_tweets = 10
    filename = 'temp_tweets.txt'
    dir_name = r'E:\Gitfolder\climate_change1'
    main()