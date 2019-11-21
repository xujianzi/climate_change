# Twitter Sentimental Analysis for Amazon Rainforest

|Author|Jian Xu|
|---|---
|E-mail|jxu109@binghamton.edu

python + tweepy + twitter API + Jupyternotebook to realize extracting tweets from the Twitter and applying sentimental analysis for the text in tweets.
***
## Reference files:

* [Project Address](https://github.com/xujianzi/climate_change)
* [Twitter Extracting](https://github.com/xujianzi/climate_change/tree/master/twitter_extracting)
* [Twitter Analysis]()
---
## Contents:
* [Project Description](#Project-Description)
* [Function Description](#Function-Description)
* [Tweets Extracting](#Tweets-Extracting)
* [Tweets Prepocessing](#Tweets-Prepocessing)
* [Tweets Analysis](#Tweets-Analysis)

---
## Project Description
This project aims to extract tweets by different users or varied keywords at a specific time spam with the mean of Python, Tweepy, and Twitter API. And we do the time analysis and sentimental analysis to the tweets data with the help of Pandas, Numpy, matplotlib.

---
## Function Description

### 1.Function Structure
![Function Structure](url1 "Function Structure Demostration")
### 2.Main fuction demostration
#### 2.1. Extracting tweets by users:
```python
def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
            tweets.append(tweet)
            print ('...%s tweets have been downloaded so far' % len(tweets))
        return tweets
```
#### 2.2.Extracting tweets by keywords:
```python
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
```   
---
## Tweets Extracting
### 1. Initialzation variables
```python
twitter_client = twitter_processing.TwitterClient()
tweet_analyzer = twitter_processing.TweetAnalyzer()
```
### 2.Extracting tweets from mutiple users(This example uses mutiple presses)
```python
    news_screen_name = ['AP', 'cnni','BBCWorld','Reuters', 'TIME', 'RT_com', 'XHNews',   
    
    'washingtonpost','Discovermag', 'cbsnews', 'bbcbreaking', 'theonion', 'mashable', 'abc', 
    
    'discovery', 'NASA','natgeo', 'theeconomist', 'cnnbrk', 'nytimes']
    news_names_list = news_screen_name
    dir_name = 'news_folder'
    tweets_nums = 20
    Path(dir_name).mkdir(exist_ok= True)
    folder = Path(dir_name)
    for news in news_names_list:
        twitter_client = twitter_processing.TwitterClient(news)
        tweet_analyzer = twitter_processing.TweetAnalyzer() 
        temp_tweets = twitter_client.get_user_timeline_tweets(tweets_nums)
        temp_df = tweet_analyzer.tweets_to_data_frame(temp_tweets)
        p = os.path.join(folder,str(news)+ r'.csv')
        temp_df.to_csv(p,mode ='a', index = False, sep=',')
```
### 3.Extracting tweets about a keywords
>Note: The system may sleep up to 5 minutes when the maxmium request is reached.
```python
def main():
    '''
    save the tweets data as jason format.
    '''
    folder = Path(dir_name)
    filepath = os.path.join(folder,filename)
    twitter_client = twitter_processing.TwitterClient(motif)
    temp_tweets = twitter_client.get_search_tweets(num_tweets = num_tweets)
    with open(filepath, 'a') as f:
        for tweet in temp_tweets:
            js = json.dumps(tweet._json)
            f.write(js)
            f.write('\n')

def users_extract():
    pass
    

if __name__ == "__main__":
    motif = "trump"
    num_tweets = 10
    filename = 'temp_tweets.txt'
    dir_name = r'E:\Gitfolder\climate_change1'
    main()
```
### 4. Program running display

## Tweets Prepocessing

## Tweets Analysis