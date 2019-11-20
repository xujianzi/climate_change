__author__ = "Jian"

import twitter_processing
from pathlib import Path
import os

def extracting_news_varibles():
    pass

if __name__ == '__main__':
    # # presses that are extracted
    names = ['AP', 'cnni','BBCWorld','Reuters', 'TIME', 'RT_com', 'XHNews', 'NBCNews', 'washingtonpost',
    'Discovermag', 'cbsnews', 'bbcbreaking', 'theonion', 'mashable', 'abc', 'discovery', 'NASA',
     'natgeo', 'theeconomist', 'cnnbrk', 'nytimes']
    news_screen_name = ['AP', 'cnni','BBCWorld','Reuters', 'TIME', 'RT_com', 'XHNews',  'washingtonpost',
    'Discovermag', 'cbsnews', 'bbcbreaking', 'theonion', 'mashable', 'abc', 'discovery', 'NASA',
     'natgeo', 'theeconomist', 'cnnbrk', 'nytimes']
    news_names_list = news_screen_name
    dir_name = 'news_folder'
    tweets_nums = 20
    Path(dir_name).mkdir(exist_ok= True)
    folder = Path(dir_name)
    for news in news_names_list:
        twitter_client = twitter_processing.TwitterClient(news)
        tweet_analyzer = twitter_processing.TweetAnalyzer() 
        #temp_tweets = twitter_client.get_user_timeline_tweets_bytime(100, young_id= 1166723685916580000)
        temp_tweets = twitter_client.get_user_timeline_tweets(tweets_nums)
        temp_df = tweet_analyzer.tweets_to_data_frame(temp_tweets)
        p = os.path.join(folder,str(news)+ r'.csv')
        temp_df.to_csv(p,mode ='a', index = False, sep=',')
        # press = twitter_processing.DftoSaveFiles(news)
        # press.df_to_csv(folder, temp_df)