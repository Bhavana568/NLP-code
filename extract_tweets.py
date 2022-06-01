# all imports
from os import times
import tweepy
from textblob import TextBlob
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random
 
#for counter in range(2):
CONSUMER_KEY='****'
CONSUMER_SECRET='****'
ACCESS_KEY='****'
ACCESS_SECRET='****'
auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
auth.secure=True
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

def extraction():

    searchQuery = 'Covid 19'
    count = 1
    try:
        # Creation of query method using parameters
        tweets = tweepy.Cursor(api.search,q=searchQuery).items(count)
        
        # Pulling information from tweets iterable object
        tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
    
    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
    
    except BaseException as e:
        print('failed on_status,',str(e))
        times.sleep(3)
        
    q=searchQuery
    tweetsPerQry=1
    fName='newFile.txt'
    sinceId=None
    max_id= -1
    maxTweets=1
    tweetCount=0
    print("downloading".format(maxTweets))
    with open(fName ,'w') as f:
        while tweetCount<maxTweets:
            tweets=[]
            try:
                if(max_id<=0):
                    if(not sinceId):
                        new_tweets=api.search(q=q,lang="en",count=tweetsPerQry,tweet_mode='extended')
                    else:
                        new_tweets=api.search(q=q,lang="en",count=tweetsPerQry,since_id=sinceId,tweet_mode='extended')
                else:
                    if(not sinceId):
                        new_tweets=api.search(q=q,lang="en",count=tweetsPerQry,max_id=str(max_id-1),tweet_mode='extended')
                    else:
                        new_tweets=api.search(q=q,lang="en",count=tweetsPerQry,max_id=str(max_id-1),since_id=sinceId,tweet_mode='extended')
        
                if not new_tweets:
                    print("no more tweets found")
                    break
                for tweet in new_tweets:
                    f.write(str(tweet.full_text.replace('\n','').encode("utf-8"))+"\n")
        
                tweetCount+=len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id=new_tweets[-1].id
        
            except tweepy.TweepError as e:
                print("Some error: "+str(e))
                break
        
    print ("Downloaded {0} tweets , saved to {1}".format(tweetCount,fName)) 


    f_1 = open("newFile.txt", "r")
    print(" The tweet is: ")
    read_tweet = f_1.read() 
    print(read_tweet)                                          

    return read_tweet
    
    
