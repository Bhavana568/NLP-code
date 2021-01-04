# MODIFIED MERGING ALL CODES 

import tweepy
from textblob import TextBlob
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import re, string, random
 
for counter in range(2):

   CONSUMER_KEY='8V4toASRqwVLXtP7yp1pKJICv'
   CONSUMER_SECRET='TDEVVQ5LBgXGzwXZKne2OAgNapIAeBSCREhLyDwvfZs8RaAO4D'
   ACCESS_KEY='1312978936037552128-NZ0WXcyfuNzJ98AbxLkuts5TVklx9h'
   ACCESS_SECRET='qJZ53s1rx6n0UUmIkjxuyXWKigF237qLCxLdPGONOjkcx'
    auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    auth.secure=True
    api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

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
        time.sleep(3)
    
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
                        new_tweets=api.search(q=q,lang="en",count=tweetsPerQry,max_id=str(max_id-1),since_id=sinceiD,tweet_mode='extended')
    
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
    #---------------------------------------------------
    
    from nltk.tokenize import sent_tokenize, word_tokenize 
    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer 
    print ("---------------------------------------------")
    tweets_extracted_from_file = read_tweet

    # remove url
    import re
    text = tweets_extracted_from_file
    pattern=r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))';
    match = re.findall(pattern, text)
    for m in match:
        url = m[0]
        text = text.replace(url, '')

    # remove mentions
    text = re.sub('@[^\s]+','',text)
    t3=text

    #def handle_emojis(t3):
        # Smile -- :), : ), :-), (:, ( :, (-:, :')
    t3 = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' Happy ', t3)
        # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    t3 = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' Laugh ', t3)
        # Love -- <3, :*
    t3 = re.sub(r'(<3|:\*)', ' Love ', t3)
        # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    t3 = re.sub(r'(;-?\)|;-?D|\(-?;)', ' Wink ', t3)
        # Sad -- :-(, : (, :(, ):, )-:
    t3 = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' Sad ', t3)
        # Cry -- :,(, :'(, :"(
    t3 = re.sub(r'(:,\(|:\'\(|:"\()', ' Cry ', t3)
 
    phrase= t3
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "cannot", phrase)

    # general
    phrase = re.sub(r"n\'t", "not", phrase)
    phrase = re.sub(r"\'re", "are", phrase)
    phrase = re.sub(r"\'s", "is", phrase)
    phrase = re.sub(r"\'d", "would", phrase)
    phrase = re.sub(r"\'ll", "will", phrase)
    phrase = re.sub(r"\'t", "not", phrase)
    phrase = re.sub(r"\'ve", "have", phrase)
    phrase = re.sub(r"\'m", "am", phrase)

    #open the fle slang.txt 
    file=open("slang2.txt","r") 
    slang=file.read() 
    ts=phrase
    ts=ts.upper()
    #seperating each line present in the file 
    slang=slang.split('\n') 
    
    tweet_tokens=ts.split() 
    slang_word=[] 
    meaning=[] 
    
    #store the slang words and meanings in different lists 
    for line in slang: 
        temp=line.split("=") 
        slang_word.append(temp[0]) 
        meaning.append(temp[-1]) 
    
    #replace the slang word with meaning 
    for i,word in enumerate(tweet_tokens): 
        if word in slang_word: 
            idx=slang_word.index(word) 
            tweet_tokens[i]=meaning[idx] 
            
    ts1=" ".join(tweet_tokens) 
    phrase1=ts1
    phrase1 = re.sub(r"won\'t", "will not", phrase1)
    phrase1 = re.sub(r"can\'t", "can not", phrase1)

    # general
    phrase1 = re.sub(r"n\'t", "not", phrase1)
    phrase1 = re.sub(r"\'re", "are", phrase1)
    phrase1 = re.sub(r"\'s", "is", phrase1)
    phrase1 = re.sub(r"\'d", "would", phrase1)
    phrase1 = re.sub(r"\'ll", "will", phrase1)
    phrase1 = re.sub(r"\'t", "not", phrase1)
    phrase1 = re.sub(r"\'ve", "have", phrase1)
    phrase1 = re.sub(r"\'m", "am", phrase1)

    punc = '''?@#$%^&*_~'''
    
    for ele in phrase1:  
        if ele in punc:  
            phrase1 = phrase1.replace(ele, "")  

    # tokenization
    t10 = word_tokenize(phrase1)

    def listToString(t10):  
        
        # initialize an empty string 
        t0 = ""
        return (t0.join(t10))           
    t0 = listToString(t10)  

    # remove puntuations
    punc = '''!()-[]{};:"\, <>./?@#$%^&*_~'''
    for ele in t0:  
        if ele in punc:  
            t0 = t0.replace(ele, "")  
    
    # NAIVE BAYES CLASSIFIER MODIFIED
    import tweepy
    from textblob import TextBlob
    import pandas as pd
    #-----------
    from nltk.stem.wordnet import WordNetLemmatizer
    from nltk.corpus import twitter_samples, stopwords
    from nltk.tag import pos_tag
    from nltk.tokenize import word_tokenize
    from nltk import FreqDist, classify, NaiveBayesClassifier
    import re, string, random

    def remove_noise(tweet_tokens, stop_words = ()):

        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                        '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens
    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))


    def get_all_words(cleaned_tokens_list):
        for tokens in cleaned_tokens_list:
            for token in tokens:
                yield token

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    
    def get_tweets_for_model(cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                        for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                        for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    classifier = NaiveBayesClassifier.train(train_data)

    print("Accuracy is:", classify.accuracy(classifier, test_data))

    custom_tweet = t0
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
    print(classifier.classify(dict([token, True] for token in custom_tokens)))

