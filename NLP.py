 

# important code
# extracting corona virus code of language english in a txt file
 
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
 
CONSUMER_KEY='gsrbo3eVv6oOqXNCcSiXT76C4'
CONSUMER_SECRET='HloviZjgUfxSQjtt0FPGwVJQEHF9brNp5wMp5sAVJNj58ywBYb'
ACCESS_KEY='1311643973669154816-jBWQJLPZXqrmnaW9LMpSFdjDy49qYU'
ACCESS_SECRET='gdxoexf4I8YgKUwJ8R6vgwIOBx1JPFzCPpw87M3TCC48s'
auth=tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
auth.secure=True
api=tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
 
##retweet_filter='filter:retweets'
##q=searchQuery+tweet_filter
searchQuery = 'Corona Virus '
count = 100
try:
# Creation of query method using parameters
tweets = tweepy.Cursor(api.search,q=searchQuery).items(count)
 
# Pulling information from tweets iterable object
tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
## print (tweets_list)
# Creation of dataframe from tweets list
# Add or remove columns as you remove tweet information
tweets_df = pd.DataFrame(tweets_list)
#print (tweets_df)
 
except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
 
q=searchQuery
tweetsPerQry=100
fName='tweets2.txt'
sinceId=None
max_id= -1
maxTweets=1000
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
 
 
#-------------------------------------------
 
 
 
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
 
def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token
 
def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)
 
if __name__ == "__main__":
 
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]
 
    stop_words = stopwords.words('english')
 
    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
 
    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []
 
    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
 
    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))
 
    all_pos_words = get_all_words(positive_cleaned_tokens_list)
    
    freq_dist_pos = FreqDist(all_pos_words)
    print(freq_dist_pos.most_common(10))
 
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
 
    ##print(classifier.show_most_informative_features(10))
 
    custom_tweet = """  b'@DonaldJTrumpJr    I heard you tested positive for the Corona virus my thoughts prayers and condolences go out to covid 19 aka Trump virus #TrumpVirus'
b'RT @zeldda: If you\xe2\x80\x99re in the health care field and don\xe2\x80\x99t believe in the gravity of the corona virus pandemic, you truly deserve to lose you\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b"@JeffreeStar If you're that afraid of Corona virus make coffee at home"
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'I just want to travel the world like Corona virus has \xe2\x98\xb9'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@PyeparFaisal But me I still use it, especially started using it to steam away this Corona virus but I use one called Dragon'
b'Simp for a tinder hoe, corona virus, a group chat destroyed by a random, pop smoke dead, capping, ceiling fans and more=2020'
b'@omar_quraishi please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'RT @LACity: Updated for 11/21:The LA City Mobile Testing Group is bringing COVID-19 testing to communities throughout the City for those\xe2\x80\xa6'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'@IPTower @johnlennon I love you John! My prayers are for the Corona virus to be gone and health is restored.'
b'@fergy1999 @XtremeUKWeather @dbirch214 I have heard that Corona Viruses are fairly stable genetically compared to say Flu. Covid is apparently 80% similar to another version of Corona Virus leading to some level of cross immunity.'
b'RT @eekhan10: @ProfKevinFenton @SadiqKhan Schools should be closed ASAP. Even school going children are having corona virus.'
b"RT @taocowboy: what's the difference between covid19 and romeo and juliet?one is the corona virus and the other is a verona crisis"
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'RT @pathbodies: Join us for our Session- Corona Virus and us @mbutler_arch @KarinaKTC https://t.co/vMsrTQsNnp'
b'Strict action is needed.. Foundation University Rawalpindi is forcing Corona Virus students to give exams.. #CloseFoundationUniCovid19 #Covid19Pakistan https://t.co/p3DZMezr4N'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @LACity: Updated for 11/21:The LA City Mobile Testing Group is bringing COVID-19 testing to communities throughout the City for those\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"@Skeptic_George @davestewart4444 Yeah! Who's ever thinking about that poor #virus? (#Corona not #TrumpJr)"
b'RT @AmyCA0214: Jr\xe2\x80\x99s testing the efficacy of coke against the corona virus. https://t.co/ta4NiR6RV1'
b'RT @irshad_rathi: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Viru\xe2\x80\xa6'
b'RT @Malik_Mehboob6: Human Version of Corona Virus..#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 https://t.co/OYJ2dbUlqy'
b'@ammaralijan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'Recovery &amp; Control by Rx TechnologyCall us for a DEMO210-828-6081#coronavirus #covid #corona #economy #stayopen #staysafe #socialdistancing #community #pandemic #virus #instagram #coronav #pandemia #memes #instagood #like #follow #solutions https://t.co/lUGxZgwzQq'
b"@MasIoob #\xda\xa9\xd8\xb1\xd9\x88\xd9\x86\xd8\xa7_\xd9\x85\xd8\xaa\xd8\xb4\xda\xa9\xd8\xb1\xdb\x8c\xd9\x85\xf0\x9f\x91\xbb\xf0\x9f\x91\x8fThank you Corona Virus'\xf0\x9f\x91\xbb\xf0\x9f\x91\x8f#\xd8\xa2\xd8\xae\xd9\x88\xd9\x86\xd8\xaf_\xd8\xae\xd9\x88\xd8\xa8\xf0\x9f\x91\xb3 https://t.co/Ip4Dn1qfNV"
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'@ammaralijan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4You Can Counter Corona Virus by Only Following Govt SOPs as No One Can Save You From this Pandemic as\xe2\x80\xa6'
b"RT @generalrich: @SherryMAGA @Jenn94314322 Is it not surprising to you? I've thought about it also my dear. It appears this Corona came to\xe2\x80\xa6"
b'RT @zgi2u1vTxg9jX2y: @CNN Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah). Imam Nas\xe2\x80\xa6'
b'@betterpakistan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'The older son of president Donald TRUMP contaminated with the corona virus'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'A Muslim remains a Muslim only.The country\'s former vice-president Hamid Ansari said: "Nationalism" and "religious bigotry" are more dangerous than "corona virus"This person never said anything to those who burst by saying "Allah hu Akbar"...#HamidAnsari'
b'RT @irshad_rathi: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Viru\xe2\x80\xa6'
b'Trump DEFENDS his country and the world in first place TRUMP ACCUSED GOV of China that provoked patented and released the CORONA VIRUS https://t.co/4omwuL6hbb'
b'RT @irshad_rathi: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Viru\xe2\x80\xa6'
b'thee amount of people I know in the medical field that don\xe2\x80\x99t believe in corona virus is terrifying'
b'RT @YaBoiCKeyz: Idk about y\xe2\x80\x99all but I refuse to take a Corona virus vaccine..... this is not Tuskegee. I will not be an experiment. Test th\xe2\x80\xa6'
b'@JoeBiden @Goss30Goss @KamalaHarris @SpeakerPelosi @SenSchumer The only way we assure relief is if we cut Mitch McConnell off at the knees! Come on Georgia! A corona virus relief package to help the middle class survive this pandemic is in your hands!!'
b'RT @aronhenny: @BreitbartNews Where is God ? Where  is justice?The Governor of NY ,  Andrew  Cuomo , on whose conscious is blood of more th\xe2\x80\xa6'
b'RT @irshad_rathi: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Viru\xe2\x80\xa6'
b'@BreitbartNews Where is God ? Where  is justice?The Governor of NY ,  Andrew  Cuomo , on whose conscious is blood of more than 11,000 senior people , who died of Corona virus , because of his mismanagement , and yet this creep in nominated for Emmy and got 25,000raise in his salary ? Wow !'
b'RT @NoemiEarly: corona virus you suck'
b'My nephews got Corona virus and it just made them more badly behaved pls is that a side effect \xf0\x9f\xa5\xb4\xf0\x9f\xa5\xb4\xf0\x9f\xa5\xb4'
b'RT @R_D_JAGDALE: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/NcCDaudtIi https://t.co/NwUynPprwm'
b"It's Absolute Madness and will be seen as such when people look back at 2020 in coming years!We have Lost Our Minds on things that have nothing to do with spreading Corona Virus and and things that actually do spread it like sitting in a restaurant for a long time people doing! https://t.co/bJumSrAaKt"
b'@Maria_Memon Ask them...what is incubation period of corona virus..means from which day..symptoms start?'
b'@StellaBeat I think it may be something that is repeated for so long, and so many times, that those who have kept hearing it accept it as a fact.Ex: Trump continuously stating that children are "immune" to the Corona virus. Well, many kids have gotten sick, and some have died.  Stupid jerk.'
b'RT @ram_durga1505: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/VzJcKduFX1 https://t.co/TqSN2rruNJ'
b'RT @reading_next: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/Tqe3g6D5DE https://t.co/1h5m2Um7QG'
b'RT @BillFriar: @RandyRainbow BREAKING NEWS: Corona Virus is now reporting that it is HIGH, really fucking HIGH on Cocaine since it came int\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b"@KagutaMuseveni Naye Kale oli fake dollar walai, You said in your own word it's fool who can organize election in Corona virus period,. The it's you who is fool now"
b'RT @Subhan_RBaloch: Corona virus is a genuine  threat but the govt: considers opposition a threat. We understand that the new container vi\xe2\x80\xa6'
b"Miami coach Diaz tests positive for coronavirus. My alma mater and I LOVE the 'Canes.... but you reap what you sow! Take the virus more seriously than the game!!  #Covid #Corona  https://t.co/cihndD01cL"
b'Antivirus Dolomite Mask "JAPAN99"\xef\xbc\x81https://t.co/1eUBWVHmSNHigh-performance mask that is more advanced than N95 mask.\xe3\x80\x9099.999% \xe3\x80\x91in 1 minute, antibacterial and removes most viruses.\xe3\x80\x9099.9% is useless\xef\xbc\x81\xe3\x80\x91#corona #coronavirus #mask #infection #virus #n95 #3M1860 #COVID19 https://t.co/tormQwbeBg'
b"I don't understand why people who know they have corona are still roaming the streets like its happy days.                                                            Like hellooo were trying to get rid of this virus, not spread it."
b'RT @GeorgiaLogCabin: Newsom [D-CA] exempts celebrities from his corona virus orders https://t.co/u7PhcRgYpv'
b'#ChooseLife .This is a tragedy among many because of Corona virus. The media trumpets cases are up!!!!! No word on hospitalizations, Covid deaths by car crash or real deaths from suicide.  The Democrats have cause untold number of deaths cause by lockdowns https://t.co/SD6F4pK6YM'
b'Amen!Treat Symptoms Not Tests!Americans have been sold a Wholesale Fraud and we just do what anyone 2+ IQ does during Flu Season and stays home if they not feeling well we stopped Lots of Deaths from Corona Virus! https://t.co/Yw7WofdBdQ'
b'@seanhannity Como \xe2\x80\x98s theatrics during the NY pandemic must of paid off for Como. He orchestrated all of the Corona virus handling in NY from his plush office at home. They forget his Bright Idea with Nursing home COVID patients an how many died. An EMMY, no way.'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'The Head of the Corona Virus Task Force @VP went to An Unmasked Rally In Georgia..  what?#StopTheInsanity'
b'RT @Subhan_RBaloch: Corona virus is a genuine  threat but the govt: considers opposition a threat. We understand that the new container vi\xe2\x80\xa6'
b'RT @laila19B: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Khyber Pakhtunkhwa Government has cancelled Rashakai Jalsa as per the directions of PM Imran Khan to con\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b'Exactly what our Stanford Doctor been saying since February which is that Asymptomatic spread of Corona Virus or Any Virus is BS and anyone with a medical degree knows this to be True and anyone participated in this Fraud needs to lose their license to practice medicine! https://t.co/g1B9seIOpH'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'Eddie jones looks like a bat, someone must have taken a nibble of him and started corona virus'
b'RT @Fantasy_lady21: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 Corona virus is   increasing day by day across the Country but the PDM Parties prefer politics ov\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus Like a Fire. @TeamISF_ https://t.co/OwfgEzBrWZ'
b'@ThisisDavina Have you missed the fact that to attend lectures in person students need to live close to the uni (usually in halls) and away from the home \xe2\x80\x9cbubble\xe2\x80\x9d. The last uni term saw hundreds of uni students confined to halls where corona virus spread rapidly. Generally- not good.'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'One new coronavirus case has been confirmed in Soite\xe2\x80\x99s area. The case has caused a mass exposure to corona virus. To ensure that classes continue, the classes at Kaustisen keskuskoulu (7-9.) will be held online during 23-29.11.2020. Read more:https://t.co/8p7JiYqlFe'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @nast_bryan: Omg \xf0\x9f\x98\xb1 she mentioned 5g and Corona virus vaccines in the same sentence! This is not going to play well in the Balkans, I\xe2\x80\x99m s\xe2\x80\xa6'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b"CHINA'S CORONA VIRUS!I received reasonable accusations against China over Corona Virus outbreaks. But Details later.AGAINNOW, Corona Virus originated from China have becomes Global horror to the world people of the all continents with annually high spreading and deaths. https://t.co/0reT2OaIxU"
b'Idk I\xe2\x80\x99ve witnessed my mom over the past few months say she is not willing to stop seeing my nephews (both of whom have had Corona virus) and my aunt pass from Corona given to her by a home health aide when she had no other visitors. There are no good choices.'
b'@ScooterMagruder no corona virus from Clemson*'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'RT @steeleleelts: @kimguilfoyle @mattgaetz @realDonaldTrump @latinos4Trump How much cocaine does it take to fight the corona virus? Asking\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'@satara657777 @miguel_biggs @Rockfang27 @GavinNewsom A virus is going to virus- if not for Corona the same people  dying form covid would have died from their other ailments or some other virus/bacteria.  Corona as Boogeyman was effective marketingas it gave a virus a technical name where as before it would be simply cold/flu.'
b'does mike dewine think corona virus is like nocturnal-'
b'@WelshGovernment I wonder why you dont look at the actual mortality rate, lockdown doesnt work masks are useless against the virus We already have anti bodies against loads of corona viruses already &amp; a lot of people it wont even affect,so there will be a public enquirey &amp; people will go to Jail'
b'Omg \xf0\x9f\x98\xb1 she mentioned 5g and Corona virus vaccines in the same sentence! This is not going to play well in the Balkans, I\xe2\x80\x99m sure a Serbian living room YouTube blogger is going to be all over this clip! \xf0\x9f\x98\x86 https://t.co/LNXYN1EADJ'
b'RT @PatsLadi99: @FoxNews Too bad he let his Revenge &amp; Ego take away his "Big"  moment where he may have made a positive pivot as a Hero in\xe2\x80\xa6'
b'Yes let all the Bible thumpers go to school. Let their god protect them from corona virus.\xf0\x9f\x99\x84 https://t.co/MwkZtVpblx'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b"@BbyBoy247 @LivesBusiness @CortesSteve You are trying to draw attention away from the large scale Dem election fraud.  Won't work.Pres. Trump Nov. 13th gave a press conference on Operation Warp Speed and the new vaccines emerging for the China corona virus.  But you rage against weekend golf. #WalkAwayFromDemocrats"
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b'@venomjunkie2 @FrankAmari2 @realDonaldTrump @SenateGOP @HouseGOP That should read "the uneducated know trump attacked the corona virus very early and aggressively". Come on now really? He has downplayed it from the start (trumps own words).'
b'@narendramodi RES SIR WE ARE TO LATE FOR TESTING PROCESS IN COVID 19 , AT PRESENT IF WE INCREASE TESTING IN COUNTRY , WE ONLY FIND MORE CASES BUT NEVER CONTROL CORONA VIRUS . IF WE DO TESTING IN EARLY STAGE ( I ALREADY TWEET IN MARCH ) WE DEFINITELY CONTROL COVID 19 BUT NOW ...'
b"@BenMack You are the brilliant 1 Ben. We haven't created a vaccine for a corona virus since first identified in 1965? What corona virus has ever disappeared? They mutate. Viruses are part of LIFE. They are foundational to OUR existence. What's the plan?"
b"RT @MRKalmati1: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to\xe2\x80\xa6"
b'RT @Satyendra_UP72: He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which no muslim like becoz their\xe2\x80\xa6'
b"Crazy how every country other than America has their corona virus situation better handled and they also gave out better/ more frequent stimulus checks Its like there's some sort of correlation or something \xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94\xf0\x9f\xa4\x94"
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'A person who was speaking and well 24 hours ago suddenly died of corona virus. Who is more stupid Pakistani people or their army? #KhadimHussainRizvi'
b'The US report more than 195,000 Corona Virus cases on Friday  a new daily high the ninth time this month a  record has been set for new confirmed infections, according to Johns Hopkins Hospitals topped 82,000 Friday, and there have been  on average 1,300 deaths a day since Sunday'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'@SaeedGhani1 Please take the dision on it very quick. The corona virus spread very fast in Pakistan every day  more than 2000 case report student life is also in danger'
b'@elonmusk what you really think about corona virus??'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b"@jenniferwilton @welt Obvious,at present all guilt to spread virus to blame community health for pandemic.Cadre's not to surrender to quarantine and dismissive  to relation restrict's I yesterday look are my centre health fight with corona Mhm?,part cadre even not to use mask  Who's make fool's with"
b'CORONA VIRUS (spreading rumors,memes ,myths) and its affect on common people due to social media . https://t.co/620BFUjWqU#CloseFoundationUniCovid19'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'@kimguilfoyle @mattgaetz @realDonaldTrump @latinos4Trump How much cocaine does it take to fight the corona virus? Asking for a friend.'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b"@wwmtnews Trump's plus the corona virus equals. https://t.co/XeVEMW5Z0W"
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Herman Cain dying of corona virus is very 2020'
b'@DannyBO23837541 @BadCOVID19Takes @atrupar This was a case of Trump Jr. infected Corona virus.'
b'@TrishKaylee @llcoolj Masks don\xe2\x80\x99t work. Corona isn\xe2\x80\x99t a bacteria, it is a VIRUS that can cut through any fabric \xe2\x80\x9cforce field\xe2\x80\x9d. It doesn\xe2\x80\x99t do anything to prevent the virus and mask wearers and social distances STILL come down with it. Same thing with disinfectants, they only prevent bacteria, not virus'
b"@thecaitdiaries Jesus could walk through those church doors and he ain't gonna save you from the Corona virus https://t.co/qejQdspWai"
b'Don Jr. has tested positive for Corona Virus. This is the first time the word positive has been used in conjunction with Don Jr.'
b'@ABC Doesn\xe2\x80\x99t matter who is that person. Stupids are surrounding us. Even worst, they can be find deep inside in our own family. These people just gave us the toughest job to convince them about the danger of CORONA VIRUS.'
b'RT @QualmesJr: Treat yourself to a few images that will make you want to stay your ass at home to protect those at risk and long for a coro\xe2\x80\xa6'
b'@ParveenKaswan Entire Residents of Thorang And Lahual Valley ,  HP ,  Tested Positive For Corona Virus . Shocking .'
b'@FoxNews Too bad he let his Revenge &amp; Ego take away his "Big"  moment where he may have made a positive pivot as a Hero in the Corona virus Pandemic! Never ever did his "Presidential Pivot" to be a real @Potus ever happen!!!! @SenateGOP https://t.co/izlXk2TpdE'
b"RT @vHariKoirala: Taking precaution to prevent corona virus infection in cold climate. Let's listen from Dr @hempaneru #NtvNews #CoronaCa\xe2\x80\xa6"
b'RT @zgi2u1vTxg9jX2y: @chrislhayes Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah).\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'RT @zgi2u1vTxg9jX2y: @CNN Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah). Imam Nas\xe2\x80\xa6'
b'Immunity from prior CV19 and previous corona virus infections, high level of T cells protecting us why do we need a vaccine, $$Billions$$ to be made by drug companies, its not about the virus! https://t.co/yeXnmcCEV1'
b'@Para_glider69 @Tactical_review and the Demo(ni)crats call us fascist. Yet they want to disarm us. Many freedoms are gone, wealth (inflation, taxes [incl property]) our homes (via corona virus $ lock down prop tax foreclosure) Wake up America.'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b"RT @DanishJui: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to t\xe2\x80\xa6"
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @Malik_Mehboob6: Human Version of Corona Virus..#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 https://t.co/OYJ2dbUlqy'
b'@FrankAmari2 @realDonaldTrump @SenateGOP @HouseGOP The smarter people know Trump attacked the corona virus very early and aggressively, Joe was against it. He had the greatest economy and jobs market in history and an excellent record on race. The idiots repeat Chinese propaganda.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@DrMuradPTI Do not take a risk on children health give the vacation and notice about corona virus then reopen school for your information the private schools are not  doing on sops they makes the children regular to come to schools'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @DanishJui: Information Minister @shiblifaraz said FIR will be registered against opposition leaders and organizers of the #PDMPeshawarJ\xe2\x80\xa6'
b'would you rather have the cure for corona virus or a real life charizard'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'@Hiromorita_ I hope in this too. Corona Virus is so annoying'
b'@HuXijin_GT Many people are forgetting that corona virus = made in China https://t.co/moivHn2FmW'
b'RT @AlisonBlunt: 1) Quote thread"Thanks to \'Corona\', many people now understand how the PCR test works &amp; will be even better able to under\xe2\x80\xa6'
b"RT @generalrich: @SherryMAGA @Jenn94314322 Is it not surprising to you? I've thought about it also my dear. It appears this Corona came to\xe2\x80\xa6"
b'Corona virus Rajasthan updates #coronavirus #coronarvirues #CoronaOutbreak #Wuhan #China #COVID19 #India #COVID #coronavirusindia  #CoronaVirusUpdate #ChineseVirus #WuhanVirus #Rajasthan #Jaipur #Jodhpur https://t.co/1iyuoRNSR8'
b"RT @ICANSouthSudan3: Some beautiful pictures coming out of today's music Recording on Corona Virus. A project proudly funded by @OxfamAmeri\xe2\x80\xa6"
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @AverageMohamed: I have lost over 27 family members across the world to corona virus. We will in the next week push a campaign against t\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Now we have 2 important medicines F0AVIPIRAVIR &amp; REMDESIVIR ... These are ANTIVIRALS that can kill the corona virus. By using these two medicines we can prevent patients from becoming severely infected and therefore cure them BEFORE THEY GO TO HYPOXIA.'
b'correct the oxygen deficiency in the blood and a better survival chance . 3. We did not have drugs to fight the corona virus in February 2020.  We were only treating the complications caused by it... hypoxia. Hence most patients became severely infected.'
b'RT @Qurat91421489: #DelayMdcat All of us are not able to fight with corona virus(Covid_19).Consider our life and our families as well.'
b"If Santa has innate immunity to Covid-19, shouldn't we be capturing him and harvesting his blood to cure and protect the rest of us from Corona Virus? \xf0\x9f\xa4\xb7\xe2\x80\x8d\xe2\x99\x80\xef\xb8\x8f"
b'RT @khanaftab9003: The United States  Corona virus caseload has now soared past 12 million. New daily cases are approaching 200,000: on Fri\xe2\x80\xa6'
b'@LonnHoklin1 @Slate Hi, I bring you a product made from the root that cures the corona virus.  It is very efficient and tested before being on the market.  We are available every day.  We deliver to your home for safety reasons, thank you.   Contact us at +22965727407 or chakracharikita@gmail.com'
b'Corona virus Gujarat updates #coronavirus #coronarvirues #CoronaOutbreak #Wuhan #China #COVID19 #India #COVID #coronavirusindia #CoronaVirusUpdate #ChineseVirus #WuhanVirus #Gujrat #Ahmedabad #Surat https://t.co/h8nkmaXnt5'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@GeorgeTakei How is it that no one else had a miraculous cure for Corona virus???'
b"@realDonaldTrump Isn't it odd that Joe Biden and his democrats don't seem to be catching the Corona(Crown) Virus. Hope round two levels the playing field and drains the swamp!"
b'No one :No fcking one :Corona Virus : https://t.co/7wCnMELtmR'
b'RT @davidaxelrod: Here is @MittRomney speaking on the #AxeFiles about the danger of @realDonaldTrump\xe2\x80\x99s lame duck actions.Full pod: https:/\xe2\x80\xa6'
b'RT @LACity: Updated for 11/21:The LA City Mobile Testing Group is bringing COVID-19 testing to communities throughout the City for those\xe2\x80\xa6'
b'RT @LACity: Updated for 11/21:The LA City Mobile Testing Group is bringing COVID-19 testing to communities throughout the City for those\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'#MythBusting"You\'re only taking bids for Corona Virus Projects "Absolutely not!We\'re incredibly proud to say that all of our grant funds have been open throughout 2020, alongside our Corona virus response pots.No suspending of applications, no pausing our funds https://t.co/H7cfiNI3Sk'
b'RT @khanaftab9003: Staggering Corona virus cases have now soared past 12 million. New daily cases are approaching 200,000: on Friday, the c\xe2\x80\xa6'
b'@BrentHBaker @jmeacham @billmaher Yeah ok, The trump administration is soooo incompetent on the corona virus that the whole Biden admin. wants trump to hand over the operation warp speed ASAP. How bout this tell Joe to come up with his own original plan for once in his life and stop plagiarizing everything!!!!'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'I hope people will donate plasma to save more lives-that could be their own loved ones! They way corona virus is spreading we need thousands of doses to treat patients. Vaccines are not treatment they are prevention not available to us as yet. https://t.co/hfmvst4etC'
b'Updated for 11/21:The LA City Mobile Testing Group is bringing COVID-19 testing to communities throughout the City for those who are unable to drive to a testing site. \xe2\x9c\x85 No appointment necessary\xe2\x9c\x85 Tests are free with or without insuranceSee more: https://t.co/ylzZNr2GtN https://t.co/rLbb3bL890'
b'@Reuters Probably Reuters don\xe2\x80\x99t know, Pakistan has stopped testing so there is no corona there, obviously China is their friend so Chinese virus will not be their enemy'
b'RT @MurphyYuiko: Florida #DeathSantis says he will not mandate any corona virus measures no matter how many of us get sick and die.Yay Re\xe2\x80\xa6'
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b"@nprpolitics Wow I didn't know that they had an award for masterfully stupid handling of the corona virus.I think he's the right man to get it though"
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@ReturnofTheJoof @jwquick Straight no chaser,  I have done many things. Your feet too small to walk in my shoes:Persian Gulf 1990-91,  6 months in Iraq.14 years of running in &amp; out of burning buildings to save strangers as a firefighter.  Taking care of Corona Virus patients.'
b'RT @Farightime: Delay mdcat students lives matter. My father is suffering from corona and after what we witnessed this corona virus is real\xe2\x80\xa6'
b'RT @CricSpartan007: Asia Cup vs IPL :Asia Cup :-Same venue UAE-6 teams vs 8 in IPL-Lesser games than IPL-International games vs T20 l\xe2\x80\xa6'
b'@politvidchannel It\xe2\x80\x99s better to rename Corona Virus to the tRump virus'
b'@realDonaldTrump Maybe it\xe2\x80\x99s karma for his sick,cowardly, psychotic killing of defenseless animals in Africa. I\xe2\x80\x99m sure his rich ass will be fine tho. It\xe2\x80\x99s not the rich that die from Corona virus, right Don??'
b'@gondalpatriot @AzmaBokhariPMLN @Patriotic_Naz @MeTalatK @shafqatchodhary @_saramunir @PTI_001 @PtiMalika @YousufKhanPti2 @Afshan_2016 @its_JaAni_ @Rabinakhan78 @mehwish_qamar6 By the way, they are very scared of Corona virus and they are no less than assholes'
b'@Mr_Pebb @JenniferRidgway @gtaldridge @AskPlayStation @PlayStation @AskPS_UK There\xe2\x80\x99s that and the factor of corona virus restrictions making it all a harder process'
b'@ABarone245 sToP bEiNg SeLfIsH!!!The Karena virus is more frightening than Corona virus.'
b'@lowkeyalbert @realPhoebe_ Hi, I bring you a product made from the root that cures the corona virus.  It is very efficient and tested before being on the market.  We are available every day.  We deliver to your home for safety reasons, thank you.   Contact us at +22965727407 or chakracharikita@gmail.com'
b'@glitterbitchh @realPhoebe_ Hi, I bring you a product made from the root that cures the corona virus.  It is very efficient and tested before being on the market.  We are available every day.  We deliver to your home for safety reasons, thank you.   Contact us at +22965727407 or chakracharikita@gmail.com'
b'@MigunaMiguna @RailaOdinga Only those with immunity against CORONA VIRUS can dare walk in streets collecting signatures. In fact the president should act with speed to announce FREE education for one year for Parents to reorganize themselves.'
b'@abc15 Arizona COVID-19 deaths/confirmed cases of Corona Virus  is 2%. Why is the number of deaths reported instead of the number of recovered cases? Trying to keep the fear factor high?'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b'Corona virus Mumbai updates #coronavirus #coronarvirues #CoronaOutbreak #Wuhan #China #COVID19 #India #COVID #coronavirusindia #CoronaVirusUpdate #ChineseVirus #WuhanVirus #Maharastra #Mumbai #Dharavi #Thane https://t.co/9GQ2yfKZsO'
b"RT @FXdestination: The 'Corona crisis' NEVER existed.The vast majority of 'Corona deaths' were nothing to do with the Corona virus.Almo\xe2\x80\xa6"
b"@SalehaMohsin @washingtonpost You can't just have the Federal Reserve doing all the work and the Senate putting forth a number of bills to help those hit hard by the Corona-virus while Nancy Pelosi along with the Democratic house sit on her hands twirling their feet saying they wants 3 trillion Dollars period"
b'Corona virus isn\xe2\x80\x99t going away. Too many people have it'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'@pradipsinhbjp @narendramodi @AmitShah @JPNadda @byadavbjp @BJP4India @BJP4Telangana @kishanreddybjp No one is wearing mask and maintaining the social distance as if they have got corona virus vaccine administered to them.'
b'Ilyas vhoraThis article about online education.The author of this article is ilyas vhora.He writes that..corona virus has closed schools for the safety of students with low immunity. This decision is appropriate for use-safe health services. https://t.co/uyHuKcmT2O'
b'RT @Seller9991: You can find various corona virus masks , dresses, socks ,etc herehttps://t.co/fDqXxgECku#dustmask, #coronavirusmask, #d\xe2\x80\xa6'
b'UP Government and Haryana Government says that the Delhi people are spreading Corona virus in UP and Haryna. Yesterday  or day before yesterday  I tweeted that this virus is being spreading in Delhi by people of UP and Haryna. Please arrange checking at borders immediately.'
b'Corona virus Delhi updates #coronavirus #coronarvirues #CoronaOutbreak #Wuhan #China #COVID19  #India #COVID #coronavirusindia #CoronaVirusUpdate #ChineseVirus #WuhanVirus #Delhi #ShaheenBagh #KalindiKunj #NCR https://t.co/OoVt7NTxka'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'@WHO My plant medicine kills all types of the micro organisms even corona virus and HIV also. I already given to so many. We are using this medicine from more than 50 years. No side effects and immediate results.'
b'RT @GeorgiaLogCabin: Newsom [D-CA] exempts celebrities from his corona virus orders https://t.co/u7PhcRgYpv'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Corona virus WestBengal updates #coronavirus #coronarvirues #CoronaOutbreak #Wuhan #China #COVID19 #India #COVID #coronavirusindia #CoronaVirusUpdate #ChineseVirus #WuhanVirus #westbengal #Kolkata https://t.co/sIzSicjKil'
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'Corona virus is really fucking up the culture lol'
b'I hope the vaccine for corona virus is safe and effective and will be out for public soon. I can\'t settle for this kind of "normal"'
b'#Health Ministry confirms 1628 new #Coronavirus cases, 10 new deaths | https://t.co/5UV975run9 | #Lebanon'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b"Taking precaution to prevent corona virus infection in cold climate. Let's listen from Dr @hempaneru #NtvNews #CoronaCare #VideoReport https://t.co/Z156rIodBN"
b'RT @tmorello: There are currently more confirmed cases of corona virus in the White House than in New Zealand, Taiwan &amp; Vietnam COMBINED. #\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'@themberjoan @Simeonie_ I recall reading how ineffective kids are @ spreading Corona virus. You must of read different research link pls'
b'RT @Bolt_Global: Corona and the Cinema Fire Arts.21 takes a look at how the virus is affecting the global movie industry Clapper boardWat\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'@dumbfinder_ @RealCandaceO @DonaldJTrumpJr I just saw on Twitter that little boy from Texas lost both of his parents. To the Corona Virus. He is going to celebrate his 5th birthday without them. The level of denial these people have is unbelievable,'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b"@beautyofhelin indeed. people are blinded by currency to the point that they revolved their world on it. it's like we're watching a horror movie where the corona virus got worsen that turned people into zombies \xf0\x9f\x91\xbb lol. that's how these #Bitcoin or any currency showed to us nowadays."
b"RT @drsmckay: I've been able to distribute a further 2 x \xc2\xa3200 grants thanks to the generosity of Leeds, our creative communities, and our a\xe2\x80\xa6"
b'@unstumpable1 @guardian It\xe2\x80\x99s a reliable way to test the presence of the Corona virus in an area. It was present in sewage in Barcelona as early as 2018'
b"Africa won't provide Corona Virus vaccine eternally."
b'RT @Farightime: Delay mdcat students lives matter. My father is suffering from corona and after what we witnessed this corona virus is real\xe2\x80\xa6'
b'We noticed that during the COVID-19 pandemic, the WP-VCD malware has also started injecting itself into plugins that can show statistics related to the corona-virus.Read more about WP-VCD malware and our analysis. \xf0\x9f\x91\x87https://t.co/rZ0wpvJbE7'
b'This is the craziest crap corona virus ,will not kill most people,Doctors are trying to get rich of this one people.'
b'RT @lubiephil: Federal operation sovereign borders are good (for dog whistling) but when it comes to states protecting its citizens from an\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @CricSpartan007: Asia Cup vs IPL :Asia Cup :-Same venue UAE-6 teams vs 8 in IPL-Lesser games than IPL-International games vs T20 l\xe2\x80\xa6'
b'RT @Farightime: Delay mdcat students lives matter. My father is suffering from corona and after what we witnessed this corona virus is real\xe2\x80\xa6'
b'RT @R_D_JAGDALE: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/NcCDaudtIi https://t.co/NwUynPprwm'
b'RT @saurabhpandeyc1: #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @ram_durga1505: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/VzJcKduFX1 https://t.co/TqSN2rruNJ'
b'RT @reading_next: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/Tqe3g6D5DE https://t.co/1h5m2Um7QG'
b'RT @Spacegirl56: @StevijoPayne His corona virus test result. That was positive. I\xe2\x80\x99m done.'
b'RT @Farightime: Delay mdcat students lives matter. My father is suffering from corona and after what we witnessed this corona virus is real\xe2\x80\xa6'
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b'@ClayTravis Neither School\'s team of Country Doctors could agree on just how fake the "Corona Virus" really is...OR... FSU after seeing the Tigers get off the bus felt they might lose more players from actually playing Clemson. #ROI #transferportal #acc #cfb'
b'RT @florida_witch: I mean corona or not I still require this space between others and now I have a valid reason when really I have been vie\xe2\x80\xa6'
b'RT @fubiz: Empty Classic Paintings to Illustrate Corona Virus Pandemic https://t.co/QVX3GWY6rw https://t.co/Im1ZohB8ZJ https://t.co/k1Y1Hxs\xe2\x80\xa6'
b'#Gujarat imposed Lockdown because Corona virus cases are being increase. https://t.co/mejGKyxrnA'
b'@mattdannatt @2jonkershaw All his 1st choice signings turned us down,the corona virus 25% deduction didn\xe2\x80\x99t help. I fear for this season. #utm'
b'Delay mdcat students lives matter. My father is suffering from corona and after what we witnessed this corona virus is really dangerous. So there should be delay. #DelayMdcat'
b'Satan Tests Positive To Corona Virus \xf0\x9f\x98\x86'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b"RT @Chalis_lokong: So there is a third wave of corona virus? It's getting tougher guys"
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b"RT @wolfgs2: Universal Peace Federation's 3rd Rally of Hope \xe2\x80\x93 'The Little Angels', South Korean Dance Troupe, Commemorating the 70th Annive\xe2\x80\xa6"
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'Swishers got me feeling like I got Corona Virus. Never again! \xf0\x9f\xa4\xa6\xf0\x9f\x8f\xbd\xe2\x80\x8d\xe2\x99\x80\xef\xb8\x8f'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'Morons all of them. Anything Trump is swimming the Corona virus. KARMA COMING https://t.co/69iSAcU9e1'
b'Community testing for corona virus in Clarkston, GA. Organized by @CoreResponse and @RESCUEorg https://t.co/aGsFBZMAhk https://t.co/JC8SUBCfNr'
b'@News3LV There is no "#corona_virus". The pandemic is a bad joke! And God Yahweh, is not, amused.'
b'@CBCAlerts Get used to it! Do not live in fear! Every one is going to get it! We have treatments that can cure corona virus! The should defund CBC, the fear monger!'
b'corona virus has done only one good thing for me, and its that i will not have to go to family gatherings surrounded by food for a while'
b'What happens when you get Corona Virus{COVID-19} https://t.co/MvQE5ueGwE https://t.co/WjNQVoyjJh'
b'RT @florida_witch: I mean corona or not I still require this space between others and now I have a valid reason when really I have been vie\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @Malik_Mehboob6: Human Version of Corona Virus..#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 https://t.co/OYJ2dbUlqy'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b"@abytw @44mmvvpp A virus has been listed, again, depending on where u google, as a microbe - i hope i don't need to post as dozen links to show u that. It's cherry picking to make a point. The fact still remains that corona no matter what u call it, is not alive."
b'@spion @LiamThorpECHO @LucasArcady @JamesPearceLFC Source? I guess the influenza virus is just much bigger than Corona virus aye?This is only important when dealing with real deadly viruses, or were you concerned about Rt Rhinovirus in past years too?'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'@ToothpasteWords You need a respirator to stop all smells. And the corona virus particles are smaller than most smells.'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @M_Wajid_H: power with in us to fight against this current situation.  Second wave of Corona virus. \xe2\x80\xa2 Wear a mask. \xe2\x80\xa2 Sanitize your ha\xe2\x80\xa6'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b"@Logical42767922 @CharlieAngusNDP What about the long haulers that incur long-lasting damage affecting every area of the body?What do you say to them? Also cite your sources regarding this being a flu. sources I've read says it's a novel Corona virus. Novel adj original and of a kind not seen before"
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'@politvidchannel I willing to rename the corona virus in his name, will that work?'
b'@OzzyOsbourne a little reminder from the pioneer of corona virus'
b'So I licked Ishcarda\'s  nose\xf0\x9f\x98\x82Her  respond: "Sies Corona virus"\xf0\x9f\x92\x80\xf0\x9f\xa4\xa6\xe2\x80\x8d\xe2\x99\x80\xef\xb8\x8f'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b"Online education is doing more torture than corona virus to students. Education shouldn't be stopped and online education shouldn't be the replacement. Please take the middle ground to solve this issue. #Shutdownallinstitutions"
b'RT @karanpujji: As the amount required is huge, I request you to kindly contribute towards the treatment and help during this time of need.\xe2\x80\xa6'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'If Chick-fil-A\xe2\x80\x99s customer service was in charge of the government the corona virus would be handled rn'
b"So there is a third wave of corona virus? It's getting tougher guys"
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'My name spread like the corona virus Shiesty in the air \xf0\x9f\x8c\xac\xef\xb8\x8f'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b"@govkristinoem Why don't you look at how successful Vermont has been at controlling Corona virus?  Guess following SCIENCE and mandating masks works! https://t.co/PbfT9xs4sC"
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'@realDonaldTrump BREAKING: The United States has now crossed 12,000,000 Covid-19 infections.America has 4.25% of the global population, but 20% of all corona virus cases, and 18.5% of all deaths.'
b'CORONA VIRUS TASK FORCE https://t.co/Cu83FUj1Y0'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'@GOP This is bs the research on corona virus has been going on for years and just needed to be tweaked. Thank scientist not trump'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b"As reports of corona virus rise in NCR, CAT 2020 should give options to change students their exam center as many of them have filled their center in Delhi and it's impossible for them to travel to Delhi now.@EduMinOfIndia @MoHFW_INDIA @JharkhandCMO @HMOIndia @IIM_I @CMODelhi"
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'RT @PandaTrickery: It is canon in the Christmas lore that the protagonist himself "Santa Claus" is immune to the Corona Virus.  Crazy plot\xe2\x80\xa6'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'RT @AnandiChetna: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https://\xe2\x80\xa6'
b'Do I need to remind All American\xe2\x80\x99s again or has the Corona-Virus mutated into a dementia?'
b'RT @muhamma93936801: #DelayMdcat The test must not be conducted in this situation.Corona Virus spreading rapidly.\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f@MJibranNasir'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @WillZembricki: If you\xe2\x80\x99re still comparing the flu to Corona virus you\xe2\x80\x99re a fucking idiot'
b'RT @ficci_india: Corona is an economic virus. It has shown the world that economies will suffer if health is not protected: Dr Dinesh Arora\xe2\x80\xa6'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'RT @KieranMaxwell: @ProtecttheFaith  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'Anybody else curious as to who in the Democratic Party got corona virus? https://t.co/DkXmOJhqfR'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @Qurat91421489: #DelayMdcat All of us are not able to fight with corona virus(Covid_19).Consider our life and our families as well.'
b'PDM\xe2\x80\x99s rally at Peshawar: it seems KP govt has started sharing actual Corona virus infection figures. The spike takes a couple of weeks to show, but KP figures show a sudden rise, which means Govt was hiding actual situation up till now.'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'RT @MaureenEMathew4: Why is it schools are to remain open where there have been instances of Corona Virus? One school had 69 students and 7\xe2\x80\xa6'
b'RT @pak_113: \xe2\x80\x9cIf corona[virus] cases are [found] on the rise because of the schools, then the government may increase the duration of winte\xe2\x80\xa6'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'Most of your food is toxic. No wonder people are getting the corona virus so easily.'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'@ArvindKejriwal @AmitShah other than emergency departments, all departments should be closed in Delhi to prevent spread of corona virus.'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'#Brockton get it together wtf the rates of corona virus keep going up.... how dumb are ya?!'
b'@RonJohnsonWI invented corona virus'
b'RT @YaeTrippy: Corona virus is at a all time high, we got the most cases &amp; deaths then any other country right now ! But y\xe2\x80\x99all clearly don\xe2\x80\x99\xe2\x80\xa6'
b'RT @debjonesdj: @Tashka9 @ValdeRazgriz @RandPaul I am so tired of the uninformed Twitter brigade who think a virus will go away if we wear\xe2\x80\xa6'
b'Why is it small stores and malls which have had no instances of Corona virus  will be closed as of Mon. Except for online shopping and curbside pickup?'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b'RT @Malik_Mehboob6: Human Version of Corona Virus..#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 https://t.co/OYJ2dbUlqy'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'corona virus you suck'
b'RT @ram_durga1505: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/VzJcKduFX1 https://t.co/TqSN2rruNJ'
b'@realDonaldTrump Thank you Mr. President for making US the corona virus capital of the world!  #MAGA'
b'RT @reading_next: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/Tqe3g6D5DE https://t.co/1h5m2Um7QG'
b'RT @R_D_JAGDALE: OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/NcCDaudtIi https://t.co/NwUynPprwm'
b'if mrbeast\xe2\x80\x99s 2020 youtube rewind will have at least 5 of the things I mention here I\xe2\x80\x99ll kill myself\xe2\x80\xa2among us\xe2\x80\xa2fall guys\xe2\x80\xa2coffin dance \xe2\x80\xa2something corona virus related\xe2\x80\xa2masks\xe2\x80\xa2iPhone 12\xe2\x80\xa2minecraft\xe2\x80\xa2dream\xe2\x80\xa2piewdiepie\xe2\x80\xa2tik tok\xe2\x80\xa2I like ya cut g \xe2\x80\xa2some random unfunny meme'
b'RT @Satyendra_UP72: He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which no muslim like becoz their\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'Santa bouta be spreadin the corona virus all over the place this year. https://t.co/hAw8Osjz3l'
b'My Corona virus vaccine free is free for all... click link to benefit https://t.co/VFwgkiGosx https://t.co/54WZnsb6IW'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b"Lol I'm not following you but clearly you're an idiot and should be blocked. Your life coach said 5G is spreading corona virus. You must be an idiot too. https://t.co/tnitq5Q0Ru"
b"RT @Auwerlmusa: You're graduate but u don't know the meaning of CV       It's corona virus..... You don't know anything \xf0\x9f\xa4\xa3\xf0\x9f\x98\x82\xf0\x9f\x98\x82"
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @TheEmployYenta: Past VP Mike Pence aka the new figure on the Cream of Wheat box and Head of Trump\xe2\x80\x99s Corona Task force campaigns instead\xe2\x80\xa6'
b'@PeterAlexander @NBCNews Does it violate HIPPA laws to say someone has corona virus when they\xe2\x80\x99re really in rehab for a cocaine addiction ?'
b"RT @Auwerlmusa: You're graduate but u don't know the meaning of CV       It's corona virus..... You don't know anything \xf0\x9f\xa4\xa3\xf0\x9f\x98\x82\xf0\x9f\x98\x82"
b'@esa @SpaceX @NASA @eumetsat @NOAA @CopernicusEU @CNES @NASAEarth @ESA_EO Looks like a bottle of Lysol on the top lol \xf0\x9f\x98\x82 are we attacking corona virus with it'
b'@GodlessIowan @GSAEmily Special shout out to the Corona virus, no one should have to deal with being infected with Don Jr...'
b'Why is it schools are to remain open where there have been instances of Corona Virus? One school had 69 students and 7 staff members test positive for corona virus.'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @KieranMaxwell: @ProtecttheFaith  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'@realDonaldTrump There is no corona virus.'
b'RT @Peacelo14780768: @GoofyOlives @sudip_ind @ignisfatuus1110 @VParamaguru1 @HarshilDholakia @HarshSanatani @DrSurabhiS_ @DoctorAjayita @do\xe2\x80\xa6'
b'@Ride_the_waves_ Of course he did. If he had been run over by a double decker bus, the Death certificate would say Corona Virus.'
b'When we see the US map of more States have Corona Virus affected. More in Mid West States. These are the places we\xe2\x80\x99re more rallies happened of President Trump.  Majority not wearing face mask.'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @Malik_Mehboob6: Human Version of Corona Virus..#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 https://t.co/OYJ2dbUlqy'
b'RT @lionsofmirzapur: @shafqat_mahmood The Fuji foundation university closed a week ago due to corona cases We cannot risk the exposure of\xe2\x80\xa6'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @suber01621030: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https:/\xe2\x80\xa6'
b"I'll be damned if I'm going to catch the virus by doing laundry. I'm being extra careful, and I don't think there's anything wrong with that. #COVID19 #COVID #ChronicIllness #PreExistingConditions #coronavirus #virus #pandemic #outbreak #disabled #mask #socialdistancing #corona"
b'call me corona virus cz no one wants me'
b"#\xda\xa9\xd8\xb1\xd9\x88\xd9\x86\xd8\xa7_\xd9\x85\xd8\xaa\xd8\xb4\xda\xa9\xd8\xb1\xdb\x8c\xd9\x85\xf0\x9f\x91\xbbThank you Corona Virus'\xf0\x9f\x91\xbb https://t.co/czb31Lnj41 https://t.co/W8aPvfeyCU"
b'Human Version of Corona Virus..#\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 https://t.co/OYJ2dbUlqy'
b'@nzain30 @SultanaSehar @anasfaisal____ @DrMuradPTI I am a student of 1st year I took 1084 marks out of 1100 marks in 10th you can verify by searching my name in FBISE site. I am supporting closure of colleges and universities because the virus is really deadly. You have a daughter ALLAH na kare ouse corona ho jae phir???'
b'did Dr. Malinga release the Corona Virus song already?'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b"RT @MRKalmati1: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to\xe2\x80\xa6"
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b"RT @drsmckay: I've been able to distribute a further 2 x \xc2\xa3200 grants thanks to the generosity of Leeds, our creative communities, and our a\xe2\x80\xa6"
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'Corona virus is at a all time high, we got the most cases &amp; deaths then any other country right now ! But y\xe2\x80\x99all clearly don\xe2\x80\x99t care lol'
b'RT @Satyendra_UP72: He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which no muslim like becoz their\xe2\x80\xa6'
b'@ZeeNews @TV9Bharatvarsh Suspected that Dragon already started Biological Warfare by spreading   Corona virus in large quantity. Spread may be similar to spread in Vuhan via single virus bottle'
b'RT @SheikhRabaiah: We need online exams to escape this virus. FOUNDATION UNIVERSITY IS THE HOTSPOT OF CORONA VIRUS CASES AND STILL TAKING O\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'Humans discriminate between rich and poor who will get the corona virus ...try my vaccine free solution, click linkhttps://t.co/VFwgkiGosx https://t.co/vNa7txnJ8g'
b'@TV9Bharatvarsh Suspected that Dragon already started Biological Warfare by spreading   Corona virus in large quantity. Spread may be similar to spread in Vuhan via single virus bottle.'
b'RT @AnandiChetna: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https://\xe2\x80\xa6'
b'OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/VzJcKduFX1 https://t.co/TqSN2rruNJ'
b'RT @lizzwinstead: Corona Virus contracted Donald Trump jr #COVID19'
b'And apparently plenty of corona virus too! https://t.co/0RREvDHAOH'
b'Yesterday at 11:00am mst, 17th prophet of this dispensation provided a video lasting exactly  11 minutes 17 seconds@NelsonRussellM also lists 7 plagues we have in society:corona virushatecivil unrestracismviolencedishonestylack of civilityhttps://t.co/u8UtuEXiBb https://t.co/NugRVsFKbB'
b'RT @saurabhpandeyc1: #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which\xe2\x80\xa6'
b"I've been able to distribute a further 2 x \xc2\xa3200 grants thanks to the generosity of Leeds, our creative communities, and our allies in our current struggles. This means an unbelievable 15 of these grants have gone out.We just need \xc2\xa360 to make that 16.https://t.co/20vtDzRE5A"
b'After corona virus attacking and wasting my whole fucking year.....NO\xf0\x9f\x98\x80 https://t.co/J9LS6Jnv7T'
b'Arthritis drug combined with remdesivir can be used to treat Covid-19 in emergency: FDAhttps://t.co/XjEVN0N8X2'
b'OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/Tqe3g6D5DE https://t.co/1h5m2Um7QG'
b'Current Conditions for #Sayre PATemp: 48.0FWind Chill: 47.2FHumidity: 74%Dew Point: 40.1F Barometer: 30.484 inHgWind: 3 mph from the NNECorona Virus Weekly Stats:Cases: 291.000000Deaths: 5.000000Survival: 98.000000#weewx #nepa #bradfordcounty'
b'Something our Stanford Doctor been saying since February on Corona Virus..."It defies everything we know about Medicine and Science to think that asymptomatic people are spreading Corona Virus...we never see that any Virus ever!"It\'s Just Total BS!  Treat Symptoms Not Tests https://t.co/1fhnJluhdl'
b'@breakingnorfolk @TheLeadCNN @izzydanzer @jaketapper People die from a lot of things.   The coronavirus is a very strange virus and more deadly than the flu.   If you don\xe2\x80\x99t think so, you haven\xe2\x80\x99t been looking at the death count of the corona virus and its symptoms.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Stop the spread of corona virus while you still can. #Shutdownallinstitutions'
b'Corona virus is definitely in any Walmart you would think about going to'
b'OSMANABAD CORONA VIRUS UPDATES ON NOVEMBER 21ST 2020 AT 6.00 PM https://t.co/NcCDaudtIi https://t.co/NwUynPprwm'
b'RT @TheNewDomShow: Donald Trump Jr something something cocaine something something Corona Virus something something'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @Seller9991: You can find various corona virus masks , dresses, socks ,etc herehttps://t.co/fDqXxgECku#dustmask, #coronavirusmask, #d\xe2\x80\xa6'
b'If we get corona virus under control next year go be so epic \xf0\x9f\x98\x82'
b'@psine_wave Ladies and Gentlemen Corona Virus has made this happen'
b'Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'have u had the corona virus?'
b'I really just can\xe2\x80\x99t friggen wait for the day when I no longer have to hear or worry about corona virus and Tr*mp'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'RT @naeem55000565: The PDM should follow the recommendations and SOPs to avoid corona virus. We r fed up due to ur non-sense activities. #\xd8\xb3\xe2\x80\xa6'
b'@realDonaldTrump Does ANYONE wonder WHY Trump never mentions what\xe2\x80\x99s happening with the CORONA VIRUS?????????   It\xe2\x80\x99s all about him not losing his position - MR TRUMP - IT\xe2\x80\x9dS LOST !!! #TrumpLegalTeam'
b'RT @MwalimChurchill: Bobi wine was charged with spreading corona virus \xf0\x9f\xa4\x94..Comedy is a stress reliever..!!'
b'#SaudiArabia always take the lead to find the solutions of the global crises, as what we see in the corona Virus pandemic #G20SaudiArabia https://t.co/GiDLuI5ClY'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @LawEnforceToday: More and more police officials are stepping up, saying they refuse to enforce the ridiculous curfew of the California\xe2\x80\xa6'
b'Corona Virus laid a Level playing ground interms of deaths..No one is safe unless we take care of  each other'
b'RT @AnandiChetna: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https://\xe2\x80\xa6'
b'Donald Trump Jr something something cocaine something something Corona Virus something something'
b'RT @saurabhpandeyc1: #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which\xe2\x80\xa6'
b'@SusanCarmona1 Yes it is phenomena and influenza being rebranded as this corona virus to up the numbers to keep people believing ,their lies , and keeping them in fear so that they will be so compliant and run to get the vaccination when it comes  ,my elderly friends and relatives - phenomena'
b'@Geeta_Mohan @BorisJohnson I m waiting to see if Trump will say ChinaVirus/WuhanVirus instead of Corona virus.  \xf0\x9f\x98\x81 #XiJinping #G20RiyadhSummit'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'@vivi_sanch Didn\xe2\x80\x99t you watch Contagion? Matt Damon\xe2\x80\x99s wife was the first victim of corona virus, they tried to warn us'
b'Dolly Parton has done more to help make a vaccine for the corona virus than Trump and his administration has.  #TrumpVirus #TrumpIsANationalDisgrace #CoronavirusPandemic #OperationWartpee https://t.co/wszdcc04fR'
b'@MochaBabe9 Or that means you had a different Corona virus. You can still test positive for the antibody but not have had covid (if that makes sense)'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b"Did zz top blow away because he didn't get his corona virus shot."
b'RT @MerrittKelly1: @kayleighmcenany Really despicable, racist remark. That tweet last month about corona virus not coming to our shores did\xe2\x80\xa6'
b'@calgaryherald If he contacted corona virus back in March how is he waiting for positive results now? Forgiveness is fate kicking you in the ass and you getting what you deserve.'
b'@moneillsf @DUPleader this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'RT @Satyendra_UP72: He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which no muslim like becoz their\xe2\x80\xa6'
b'@ifbacongrewont1 @44mmvvpp No, I never said corona is a bacteria. It\xe2\x80\x99s a virus.This is what I said: https://t.co/4pnIQ56QlE'
b"Law enforcement justified in refusal to enforce California's curfew (op-ed) https://t.co/LSWTKyYYGT"
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"@Dan31609301 @LeadersMaster @TrumpWarRoom Trump is a fool who could not manage corona PR. B4 CCP virus, trump leads for 2nd term. Still he won elections. For sure almost near margins tells election fraud happened. It's really sad America turning more like left radical anarchy state. SHE of China would be partying now."
b'RT @LawEnforceToday: More and more police officials are stepping up, saying they refuse to enforce the ridiculous curfew of the California\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @MwalimChurchill: Bobi wine was charged with spreading corona virus \xf0\x9f\xa4\x94..Comedy is a stress reliever..!!'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'@realDonaldTrump @Dr_sarakhan1 Kindly also allowed Pfizer  corona virus vacations for PAKISTAN.'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'@amitsurg @NaIna0806 @ARanganathan72 @dasgobardhan is compromised and incompetent @WHO one of big challenge in fight against wuhan/ corona virus?'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b"RT @Auwerlmusa: You're graduate but u don't know the meaning of CV       It's corona virus..... You don't know anything \xf0\x9f\xa4\xa3\xf0\x9f\x98\x82\xf0\x9f\x98\x82"
b'@Raktotpal2 @PratyoiB He was back then  being alleged of over rating the corona virus....but not even a single voice strongly stood for his actions for the well being  of the people...But for criticism... well we have a several voices... dont we???@himantabiswa'
b'Imran Khan and Pakistan army is using Corona as NAB against opposition parties of Pakistan. Was Corona virus on holiday on Khadim Rizvi Janaza ?'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'If corona virus shut down planned Parenthood it would save more lives than it\xe2\x80\x99s killed.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b"@CJ14408715 @abc13houston The cdc changes it's recommendations as more information and data becomes available.   This is a novel/new strain of the corona virus.  One would expect recommendations to change. FACTS MATTER!"
b'@oneminutecall Wow! I\xe2\x80\x99m glad you had the whole tray re-made. I would think @Starbucks head office would want to know about this and clamp down. Clearly some locations and staff did not get the memo.So sad that some people want to live with the corona virus forever.'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'@MeidasTouch Why are they sooooo angry I realllly think this CORONA VIRUS BRING OUT HATERED IN HUMANS\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba\xf0\x9f\xa5\xba'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'@stitchious Russia is done with testing now. It is now offering Sputnik corona virus vaccine to many countries including SA corrona. Putin says. We looking forward to the move and flop that will be made by SAgov on this offer. New world order is here while media is buzzy focusing at ubaba https://t.co/F0pez9n1qa'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'Am so saddened by the loss of front line medical practitioners due to Covid 19. This trend is worrying. As a country there is need for us to do more to fight this pandemic especially in what can be seen to be a second wave of the novel Corona Virus. Condolences to the bereaved.'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'@Tandav__ @OpusOfAli Yes unfortunately 5000 years+ still discovering... corona virus vaccine invented by Turkish doctors unfortunately did not come from Gau mutra \xf0\x9f\x99\x8f'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'Gotta love politicians who downplay the corona virus! https://t.co/ZtCx2GFxb4'
b"China will be the bad guy in everything. Corona virus. Radar technology to nail US fighters. The newspaper that described that was founded by a India IIT University student. IIT University's r like the US' MIT. They have lots of them."
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'@MollyJongFast @pattykanan Corona Virus is much smarter than everyone going to that party...'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b"RT @MaChiJune1993: @gmcantave1 The assumption that all songs have to be about love it's staggering on itself. But like, dude\xe2\x80\xa6 you have frea\xe2\x80\xa6"
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b"RT @MRKalmati1: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to\xe2\x80\xa6"
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b'RT @Tahirchaudhary_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly\xe2\x80\xa6'
b"@drsheikhRSS Please make a video on how China's currency manipulation is exposed due to less growth in gdp due to Corona virus pandemic"
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'RT @AlisonBlunt: 1) Quote thread"Thanks to \'Corona\', many people now understand how the PCR test works &amp; will be even better able to under\xe2\x80\xa6'
b"We don't want to become the reason for spreading corona virus.#CloseFoundationUniCovid19  Exams should be online"
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'RT @MaqsoodHashmii: Huge gathering for funeral of Khadim Hussain Rizvi without any SOPs, where is PTI Govt will it not spread Corona Virus.\xe2\x80\xa6'
b'are you ready for nyt articles next year like "a vaccine has been widely available for months, so why are we still seeing corona virus deaths across the country?" before sympathetically profiling a bunch of antivaxxers in pa and ok that have killed their own loved ones'
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'@cnnbrk If he dies of corona virus I very much doubt his father will change'
b"Cont'd: Tell them their health and health of the families are very important SO take all the gears while going to Jalsa so that Jalsa goers protect themselves and their families by this evil virus CORONA"
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'RT @rohini_sgh: Another nonsensical decision. Corona doesn\xe2\x80\x99t strike at night. Govts should instead be looking at strictly implementing wear\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'3934967 people recovered from Corona today. Total Corona virus recoveries: 39590865   Source: WHO Situation Reports  #COVID19 #coronavirus #StaySafe'
b'RT @Qurat91421489: #DelayMdcat All of us are not able to fight with corona virus(Covid_19).Consider our life and our families as well.'
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b"@morethanmySLE @joncoopertweets I no longer time exactly, how's substantce, have a \xf0\x9f\x92\x89 Corona virus, and How chromosome, and genotype thiss my viruses have. https://t.co/O3cc1VbtZX"
b'RT @nomi6006: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The @MaryamNSharif is a corona , be carefull this type of virus, she is very talented in patwaripan, @T\xe2\x80\xa6'
b'... let me watch The Walking Dead so I get all the tips cuz goodness gracious this Corona virus is showing true colors of everyone'
b'This thread is outstanding source on corona virus screw ups &amp; timelines https://t.co/kvUzoYnDau'
b'RT @FarahK__han: I\xe2\x80\x99m not in the favour of delay but i\xe2\x80\x99m also not in the favour of conducting paper illegally and conducting it amid the cor\xe2\x80\xa6'
b'@RobertVonAllen @thehill Do you understand the difference between dying from COVID and dying with corona virus in your body?Because both are in the 250k.'
b'RT @khanaftab9003: Staggering Corona virus cases have now soared past 12 million. New daily cases are approaching 200,000: on Friday, the c\xe2\x80\xa6'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'RT @Qurat91421489: #DelayMdcat All of us are not able to fight with corona virus(Covid_19).Consider our life and our families as well.'
b'RT @Satyendra_UP72: He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which no muslim like becoz their\xe2\x80\xa6'
b'@michellelauer24 @PurpleGlamQueen @komonews FYI Corona is a common cold strain. Why doctors say it is not a flu virus. By chance did you shop at a super spreader center like walmart?'
b'RT @TheEmployYenta: Past VP Mike Pence aka the new figure on the Cream of Wheat box and Head of Trump\xe2\x80\x99s Corona Task force campaigns instead\xe2\x80\xa6'
b'RT @SheikhRabaiah: We need online exams to escape this virus. FOUNDATION UNIVERSITY IS THE HOTSPOT OF CORONA VIRUS CASES AND STILL TAKING O\xe2\x80\xa6'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'If you\xe2\x80\x99re 1 of the few who like my Corona Crash posts, I\xe2\x80\x99m curious why?Personal portfolio performance &amp; trade highlights?Identifying memos/writers unknown to you?Unique reference for the future or for current virus &amp; macro news?How about the things you don\xe2\x80\x99t care for? https://t.co/W4sWJQsyH6'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'@realDonaldTrump Stop fixating on nonexistent voter fraud!There are millions of people going hungry and are in dire straits! Concentrate on helping the people in our nation who are suffering due to the CORONA. Virus! People need a Stimulus package! Quit being a narcissistic ass and help us!'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b"@Prachigauniyal @BTS_History613 @BTS_twt Well I'm a second year Med student\xf0\x9f\x99\x82with this shitty corona virus and online classes we couldn't study anything properly and whole year was like self study and now University suddenly declared our exam out of blue\xf0\x9f\x98\xad"
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'@ImranKhanPTI @WHO good way to spread Corona Virus \xf0\x9f\xa6\xa0 everywhere what a splendid job by Pakistan and @ImranKhanPTI Administration he speaks of everything but never \xf0\x9f\x91\x8e practices it in his own country frm Human Rights to minorities safety to Covid-19 safety measures what a loser! https://t.co/OTzVkd6P7E'
b"RT @MaChiJune1993: @gmcantave1 The assumption that all songs have to be about love it's staggering on itself. But like, dude\xe2\x80\xa6 you have frea\xe2\x80\xa6"
b'RT @Asuka_Boi: Jan 2020:&gt;Possible WarFeb 2020:&gt;Kobe\xe2\x80\x99s PassingMarch 2020:&gt;Corona VirusApril 2020: https://t.co/nlLSgCZ1p4'
b'@drdavidsamadi if the common cold is a Corona Virus, and you have cold symptoms and get a Covid quick test, could it give a possible false negative?'
b'RT @14Rehmatullah: As you all know Corona virus cases are increasing so much in Sindh Agricalture University Tando Jam almost 70 cases have\xe2\x80\xa6'
b'RT @MadamShurli: How mental is it? I am not worried about corona but actually the extremism and illiteracy which is propagating faster than\xe2\x80\xa6'
b'#DelayMdcat All of us are not able to fight with corona virus(Covid_19).Consider our life and our families as well.'
b"@H_MitchellPhoto @DonaldJTrumpJr Yes Jr, stay corona virus positive so we don't have to see or hear you anymore please don jr"
b"I've decided I want the Corona virus. I dont have much of a personality so I'm willing to become the Corona virus guy"
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'RT @JuneOwe98467910: @LS3370 @HeavenlyMalbec @BloodyPolitics @NicolaSturgeon @theSNP She asked us yesterday why she (or any government) wou\xe2\x80\xa6'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'RT @zgi2u1vTxg9jX2y: @CNN Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah). Imam Nas\xe2\x80\xa6'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'@CNN Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah). Imam Nasser Mohammad Al-Yemeni05 - 03 - 2020 AD covid-19 vaccineCoronavirusBiden Harris TrumpSaturday morning'
b'@DrMuradPTI Sir corona virus is not editable disease it remain at all but our education process become low day by day because exams are  near if school college will be closed then we will face A lot of loss'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'The City of Dallas has a #COVID19 Resource and Information website, and hotline for you to get all the latest and up to date information. (214) 670-INFO (4636). https://t.co/t1BdhfuyNT https://t.co/s0jAD7Cpms'
b'RT @muhamma93936801: #DelayMdcat The test must not be conducted in this situation.Corona Virus spreading rapidly.\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f@MJibranNasir'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b"RT @Fatimah62615556: Foundation university rawalpindi campus has become the hotspot of Corona virus but still they're taking on campus exam\xe2\x80\xa6"
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'RT @zgi2u1vTxg9jX2y: @chrislhayes Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah).\xe2\x80\xa6'
b'@chrislhayes Corona-virus is from the minor chastisement before the major chastisement so they may turn(to Allah). Imam Nasser Mohammad Al-Yemeni05 - 03 - 2020 AD covid-19 vaccineCoronavirusBiden Harris TrumpSaturday morning https://t.co/9FTSphbnF5'
b"RT @bachpanamitabh: WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b"WHO may help with Corona Virus but for M@di Virus even they would be asking WHO let's the dogs out."
b"The Palouse = Eastern Washington where Washington State is at in Pullman is eaten-up with Corona Virus and never in a Zillion Years would we have thought folks in Palouse, Idaho, Montana, Dakotas, Wyoming wouldn't have Common Sense slow spread Corona Virus...It's So Damn Easy! https://t.co/Nm1xY5XQjb https://t.co/gMTR0ZvVRD"
b'@henryshield @atiku My annoyance was his donation to the federal government during the corona virus. Why not get to the masses on his own by sharing the palliatives to the people instead he enriched those that has impoverished the masses.'
b'@ChrisCuomo Lol. Says the guy who faked having Corona Virus. You are a hypocrite and a bigot. That is a fact sweetheart.'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @AlisonBlunt: 1) Quote thread"Thanks to \'Corona\', many people now understand how the PCR test works &amp; will be even better able to under\xe2\x80\xa6'
b'@realDonaldTrump @MaxwellOkafor6 They should add corona virus result to his votes by then he will win.George Bush caught Saddam HusseinObama caught Osama Bin LadenDonald Trump caught what!!!!!  corona virus\xf0\x9f\x98\x83\xf0\x9f\x98\x83\xf0\x9f\x98\x9b\xf0\x9f\x98\x9b'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'@ScottAdamsSays China "beat" the Corona virus the easiest way. Don\'t give a Dick about your people, and be happy it "Thins out the herd" a bit. The old, sick, and weak. China would be happy if it didn\'t make the whole world hate them. 1.4 billion. They have plenty to spare, and don\'t care.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @suffernaamaa: #Shutdownallinstitutions i dont wanna die of corona virus i want it to be smthn cool so plis'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"@charliekirk11 Its called the Corona virus. By the entire world exect the few shoppers that regurgitate the nonsense that falls outta the 45th lovers mouth.  I'm sure your buddy Jesus wouldn't like you being malicious."
b'#Shutdownallinstitutions i dont wanna die of corona virus i want it to be smthn cool so plis'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b"@nytimes When did science disappear I didn't know it was possible for a healthy person to get another healthy person sick with corona.... The fear of rona is going to start being more dangerous then the virus itself"
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'Regardless of any position,a Muslim remains a Muslim onlyThe country\'s former vice-president Hamid Ansari said"Nationalism"and religious bigotry"are more dangerous than"corona virusThis person never said anything to those who burst by saying"Allah hu AkbarThey are only traitors'
b'RT @MwalimChurchill: Bobi wine was charged with spreading corona virus \xf0\x9f\xa4\x94..Comedy is a stress reliever..!!'
b'Y\xe2\x80\x99all be like \xe2\x80\x9cI can\xe2\x80\x99t believe they\xe2\x80\x99re trying to take away thanksgiving\xe2\x80\x9d like THEY you mean fucking corona virus not the ppl trying to deal with this pandemic you imbisals'
b'My mom had corona virus and she didn\xe2\x80\x99t even tell anyone \xf0\x9f\x98\x82'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'@washingtonpost Mister Nurs. This Viruses have 4 ghenesys, or GHENOME, genotype. Decode every type Covid19, genotype, 4. And after decoding the comletly Corona virus, I giviging American Infectolog, than RIGHT SUBSTANCES vor 2 type Injekton, one injection \xf0\x9f\x92\x89, are too helping infected people. https://t.co/JwCnuIrMiK'
b'RT @Seller9991: You can find various corona virus masks , dresses, socks ,etc herehttps://t.co/fDqXxgECku#dustmask, #coronavirusmask, #d\xe2\x80\xa6'
b'RT @KINGKONG30001: @LeadersMaster @ChrisCuomo "We will not see diseases like the corona virus come here."  - Kayleigh McEnany February 25th'
b"Some beautiful pictures coming out of today's music Recording on Corona Virus. A project proudly funded by @OxfamAmericaWe thank Bazande Pictures Media for the great and professional coverage. Stay tuned @RadioMiraya @EyeRadioJuba @OxfaminUganda @oxfamibis @Radio https://t.co/KtDFtuq8UU"
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'A novel coronavirus (CoV) is a new strain of coronavirus.The disease caused by the novel coronavirus first identified in Wuhan, China, has been named coronavirus disease 2019 (COVID-19) \xe2\x80\x93 \xe2\x80\x98CO\xe2\x80\x99 stands for corona, \xe2\x80\x98VI\xe2\x80\x99 for virus, and \xe2\x80\x98D\xe2\x80\x99 for disease.   #coronavirus #COVID19 https://t.co/YrSMv1k6OZ'
b'RT @SheikhRabaiah: We need online exams to escape this virus. FOUNDATION UNIVERSITY IS THE HOTSPOT OF CORONA VIRUS CASES AND STILL TAKING O\xe2\x80\xa6'
b"RT @DanishJui: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to t\xe2\x80\xa6"
b"RT @FXdestination: The 'Corona crisis' NEVER existed.The vast majority of 'Corona deaths' were nothing to do with the Corona virus.Almo\xe2\x80\xa6"
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b"My brother most likely has corona virus. Which means I'm about to square off with the Mandarin miasma itself. So.... we finally meet. https://t.co/J8Gz7sU4oH"
b'RT @RozineCapt: OKAY.....Influenza is a Corona VirusBut Nobody Has IT??? \xf0\x9f\x98\xb7\xf0\x9f\x99\x84'
b'@globaltimesnews  hi global times, were you able to find the source of corona virus??? If not, i hv a clue fr u, lick asshole of xi zing ping, and hold his penis , virus will come out, immediately put mask on his penis.head of global times , u are #GUH#'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"@gmcantave1 The assumption that all songs have to be about love it's staggering on itself. But like, dude\xe2\x80\xa6 you have freaking text in front of you\xe2\x80\xa6 It's a song about the pandemic, where the hell is the 'girl'... This isn't the song version of that book that ships YN with the Corona virus"
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'We need online exams to escape this virus. FOUNDATION UNIVERSITY IS THE HOTSPOT OF CORONA VIRUS CASES AND STILL TAKING ONCAMPUS EXAMS FROM 23RD!!SAY NO TO ONCAMPUS EXAMINATION!#CloseFoundationUniCovid19'
b'@ReneeAlida He will be wiped out like the Trump virus, er I mean Corona virus \xf0\x9f\xa4\xaa'
b'@realDonaldTrump Bro you lost, give it a break. We want to hear what you\xe2\x80\x99re doing about the Corona virus.'
b'so many corona virus deaths in america but donald trump just ignores them, the public doesn\xe2\x80\x99t matter, it\xe2\x80\x99s all about HIM, he\xe2\x80\x99s just tweeting about himself and how he won the election \xf0\x9f\xa4\xa6\xf0\x9f\x8f\xbc\xe2\x80\x8d\xe2\x99\x80\xef\xb8\x8f\xf0\x9f\xa4\xa6\xf0\x9f\x8f\xbc\xe2\x80\x8d\xe2\x99\x80\xef\xb8\x8f'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b"This Isn't About A Generated Computer Program CALLED CORONA VIRUS It's a Targeted ATTACK on World's Economy The Reprogramming of Peoples WAY of thinking NO ULTRA MIND CONTROL from Gates Computer States Leading Programmer Plus DNA DATA GATHERING BLOOD DATA for Depopulation5G\xf0\x9f\x8e\x89\xf0\x9f\x8c\x8e\xf0\x9f\xa4\xa0"
b'85 new corona virus cases in #Tonk, RajasthanTotal Cases in district 2305'
b'Unilever to launch mouthwash that eliminates 99.9 pc corona\xc2\xa0virus https://t.co/rQnvQHQ3Cj'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'\xf0\x9f\x98\x87\xf0\x9f\x87\xa8\xf0\x9f\x87\xa6 2nd lockdown to reduce de  corona virus 19 cases.'
b'RT @carolinahawkins: UK AmbassadorSpecialist Practioner and Expert Caroline I will be helping you Recover Corona Virus Flu Game and get yo\xe2\x80\xa6'
b'Jumping into the pool: How to earn a profit mining Bitcoin and Ether#latest_update_corona_virushttps://t.co/0SEZ4qUYu8'
b"@AggreyTim @muhumuzamichel @EngMosesEddieTi @DavieFinal @DavidDallas256 @frank_muhanguzi @CatalanCeleb @Griffin2567 @Koma_Flemmings It's Corona virus coz it's a microscopic pathogen that causes covid19"
b'@Girish0830 Sometimes I wonder if their spray or liquid can kill Corona virus why cnt we drink it?'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'@utdreport Thank god don\xe2\x80\x99t need any virus we already suffering from corona'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'The irony that Guilliani is in quarantine and can\xe2\x80\x99t personally appear for his shitshow court cases is hilarious.    So much for the Corona Virus will go away after the election and nobody will care prediction.  #coronavirus #COVID #Election2020results #StopTheSteaI #LoserInChief'
b'CORONA Virus is increasing and FUIC has many positive cases but still student are forced to appear physically on campus for exams .Many students have flu, cough and fever . Our lives are at risk .#CloseFoundationUniCovid19'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'So we can pinpoint that people are getting the corona virus from church but can\xe2\x80\x99t pinpoint where trafficked children are being taken??? Suuuuuspect...'
b'@CNNPolitics And Trump is off to the golf course again while ignoring people dying from Corona virus, millions unemployed, thousands of businesses closed, long lines waiting for food, and a flood of evictions to come.'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b"@mareawinyfridah Like covid19 and corona virus ain't the same"
b"@MelvaV5 @TheInterwideWeb @thebradfordfile He hasn't attended a corona virus briefing in 5 months."
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b"RT @Fatimah62615556: Foundation university rawalpindi campus has become the hotspot of Corona virus but still they're taking on campus exam\xe2\x80\xa6"
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'@eileendt5 @brikeilarcnn True, an American trait. Blame everything else. Force opinions on others. Covid19/Corona virus is the killer, period. Lack of medical protection. And the horror of having to be exposed. "Plain simple honest language", (George Carlin)Thank you, Ms.Eileen'
b"The 'Corona crisis' NEVER existed.The vast majority of 'Corona deaths' were nothing to do with the Corona virus.Almost all Western governments are using this fake 'crisis' as the tool to install Police State controls, &amp; to inject everyone with their gene-altering 'vaccine'. https://t.co/PQy8UBZ3xr"
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'@neiltyson True...humans discriminate, Creator does not with his vaccine free Corona virus solution https://t.co/kIhbqWHseu'
b'RT @jaybhanushali0: Thank you CMOMaharashtra Aaditya Thackeray ji for being there for one &amp; all. Centre to adapt Mumbai model to fight CORO\xe2\x80\xa6'
b'I just need my corona virus test \xf0\x9f\x98\x96'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b"@BenGilroy11 Just like the pic on Leo's computer about the sale of PPE for Corona back in 2018.. The virus ( scamdemic) nothing to do with health it's control.."
b'RT @SheikhRabaiah: Health before anything! We can not put our families at risk. BAN ONCAMPUS PAPERS AS OUR FOUNDATION UNIVERSITY IS THE HO\xe2\x80\xa6'
b'@MSNBC If this is true then everyone in america has corona virus,get real ,stop the lies.'
b"Foundation university rawalpindi campus has become the hotspot of Corona virus but still they're taking on campus exams, say no to on campus exams. #CloseFoundationUniCovid19"
b'Toddler in Chief still politicizing Corona Virus, also he had nothing to do with the development of vaccines despite his claims. Trump turns on Pfizer over vaccine timing https://t.co/DuJ3uNx9bA via @YahooNews'
b"RT @MRKalmati1: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to\xe2\x80\xa6"
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'News flash.  Everybody is going to get the China-Corona flu..   You can\xe2\x80\x99t stop it. It\xe2\x80\x99s a virus. And if your under the age of 80 you have a higher probability of dying from a car accident then this strain. You all enjoy Big Brother suffocating your right to freedom and liberty!!'
b'RT @SheikhRabaiah: In this time of pandemic, where FOUNDATION UNIVERSITY RAWALPINDI CAMPUS has become the hotspot of corona virus, they hav\xe2\x80\xa6'
b'@DonaldJTrumpJr Gotcha...  Well done Jr.  Don\'t die from Covid.   Only "nobodies" get Corona Virus.  Right Jr.... Nobody!  Get back on your stump. https://t.co/POj9BwPrhs'
b"@RudyGiuliani That wasn't hair die running down his face. It was the Corona virus!!\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3\xf0\x9f\xa4\xa3"
b'Corona is a real virus-many say it is not so they have an excuse to not wear masks.  Wearing masks around others prevents the spread.   The evil deep state is behind corona too.  Killed many and did big damage to the economy.'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'In this time of pandemic, where FOUNDATION UNIVERSITY RAWALPINDI CAMPUS has become the hotspot of corona virus, they have decided to take on campus exams from 23rd November, say no to on campus exams.!!!SAY NO TO ONCAMPUS EXAMS IN THIS SITUATION !#CloseFoundationUniCovid19'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'We could also, in his honor, rename the virus, no longer call it corona or covid, but Trump ! https://t.co/9ekzTzRxqR'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'@Protegeofhim @beefybalfe @MichaelBina @ShannonWaycast1 @the_resistor @realDonaldTrump And you think that\xe2\x80\x99s an appropriate thing for the President to say, on live TV, during a corona virus press conference?'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'"Food was delicious.  We did take out because of corona virus restrictions - but we saw they did have heaters on their outdoor patio.  Online ordering worked great and our food was ready when we arrived to pick it up." says N on Google, via @Birdeye_ https://t.co/PO8CpqvADT'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @SheikhRabaiah: Health before anything! We can not put our families at risk. BAN ONCAMPUS PAPERS AS OUR FOUNDATION UNIVERSITY IS THE HO\xe2\x80\xa6'
b'RT @rudra94823323: In this Corona pandemic situation GTU had decided that the exam will be taken offline and also another side the epidemic\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @lionsofmirzapur: @shafqat_mahmood The Fuji foundation university closed a week ago due to corona cases We cannot risk the exposure of\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Health before anything! We can not put our families at risk. BAN ONCAMPUS PAPERS AS OUR FOUNDATION UNIVERSITY IS THE HOTSPOT OF CORONA VIRUS CASES!We can give ONLINE EXAM. #CloseFoundationUniCovid19'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'@ajpeebles @Ryan_Burgio @PatrickBaitman3 @saxena_puru I bought it between October 13-19 in small chunks. Some down days as you said and I had to take a small loss and sell it on October 29.Your thesis may be right that $LSPD faced sector specific correction/Corona virus news then. I just want to test it a bit more.'
b'Pre corona virus is days are SOO last decade.'
b'GONDIA CORONA UPDATES:Gondia district witnessed 150+ COVID-19 cases today for the first time in October-November months while 105 patients defeated corona virus today. Due to increasing number of cases &amp; testing, reports of 908 samples are awaited from RT-PCR lab.#\xe0\xa4\x97\xe0\xa5\x8b\xe0\xa4\x82\xe0\xa4\xa6\xe0\xa4\xbf\xe0\xa4\xaf\xe0\xa4\xbe https://t.co/JtZpb2ZQuL'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b"RT @DanishJui: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to t\xe2\x80\xa6"
b'RT @hungryfor_books: Pandemic is an AMAZING game! Buy: https://t.co/sFQ7ZJDhkc#ad #boardgames #boardgame #boardgamegeek #games #familyfun\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @lionsofmirzapur: @shafqat_mahmood The Fuji foundation university closed a week ago due to corona cases We cannot risk the exposure of\xe2\x80\xa6'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'@hari_singh_go @globaltimesnews You called : so called Five eyes alliance , even Working for the Betterment of World unlike China. But you have not Put up any Historical references from Historical  Ongoing records. How Do you Claim in Answer to Marco Antonio Flores ? Chinese Corona virus Free World . you o.k.'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'It\xe2\x80\x99s honestly wild to see the beginning of the corona virus play out on reality tv....'
b'always stay away from the Anti-kirant culture,Who has been tirelessly effort to demosing that his own supernatural kirant history  to spreading many confusion and rumour without any proof,actually they are very dangerous virus than recent corona virus pandemic those people----'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @davidaxelrod: In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the lat\xe2\x80\xa6'
b'RT @Richard_L_Lara: @thehill Or we could name it The Fallen, to honor those who did not survive the Corona virus. This would be far more ap\xe2\x80\xa6'
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b'Enjoying coffee...slept in for the first time in a while! It feels good to get some good sleep. Easier to sleep because I know @JoeBiden has a plan to help us through corona virus pandemic!'
b'@DrMuradPTI Sir decide whatever is best suited to the health of teachers and students and education as well.. You knows better facts and figures regarding corona virus then us.. Your decision will be heartly welcomed. We trust you fully... God bless you sir'
b'In summer, @MittRomney surprised many when he joined a Black Lives Matter march in DC.  I asked him about this on the latest #AxeFiles.  His personal, poignant answer may surprise you.Full pod here \xf0\x9f\x91\x89https://t.co/2oZsMhHW0s https://t.co/xwh4BiXF8V'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'@margiegem A sense of invincibility or pure ignorance? Sooner or later, there will be a "figure skating cluster" spreading the corona virus.'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'@Acyn @jkola13 How about we rename the corona virus the Trump Virus and every time someone is vaccinated against it they yell \xe2\x80\x9cFuck Trump!\xe2\x80\x9d Works for me.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'king if you want to blame somebody for all these peoples deaths from the corona virus just look at joe biden and his son hunter , they had china to make up this virus in a lab just for this election they are the ones dealing with china they will find it to be true to before long'
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"@starsandstripes @jaketapper it's amazing how we are the largest advanced country in the world and we're doing the worst with the Corona Virus! and citizens not having food?! all under the @POTUS admins. we need @JoeBiden fast !!!!"
b'RT @djkaywise: Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'Club last night was crazy and choked I guess no more Corona virus in Lagos \xf0\x9f\x87\xb3\xf0\x9f\x87\xac Ose olorun mi !!!! \xf0\x9f\x92\xb0\xf0\x9f\x92\xb0\xf0\x9f\x92\xb0 #JoorNation'
b'RT @mpolikoff: Super cool opportunity to add questions (for free!) to the @UAS_CESR Understanding Coronavirus in America (longitudinal, nat\xe2\x80\xa6'
b'RT @Quea_Ali: This goes well beyond whats needed, Christmas is coming does the government not realize that? No amount of corona virus chang\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"Whatever It Is, It\xe2\x80\x99s Probably Not Hair Dye https://t.co/x23eB8dc4c It's the CORONA VIRUS Aside from his water brain from alcoholism, this idiot has the covid sweats and is oozing the negativity juice from his cosmetically challenged dirty ass cranium."
b'@Shafqat_Mahmood @DrMuradPTI please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down. https://t.co/5KuaolxgQS'
b'RT @JibbyD: You know... if you are posting about how concerned you are about Khadim Rizvi\xe2\x80\x99s funeral being a super spreader, but are complet\xe2\x80\xa6'
b'Cloth Face Masks Only 9.99! \xf0\x9f\xa5\xb3https://t.co/hpICnGkYXX #cloth #face #mask #buy #sale #health #corona #virus #coronavirus #pandemic #patient #diseased #hospital #christmas'
b"New York Gov. Andrew Cuomo scores International Emmy Award for coronavirus briefings \xe2\x80\x94 to Meghan McCain's chagrin    He deserves it because he kept us informed and encourages us all during the  Corona virus  carnage https://t.co/GbwoWrhY0l"
b'@CNN QUIT all your GOOD habits of Smoking, Alcohol, Drug, PORN, Premarital Sex/Extramarital Affair..to make yourself mentally &amp; physically healthy..to make your immune system STRONG..to avoid attacks of any virusGROW UP at least after facing this Corona..Until vaccine gets invented.'
b'@CNN QUIT all your GOOD habits of Smoking, Alcohol, Drug, PORN, Premarital Sex/Extramarital Affair..to make yourself mentally &amp; physically healthy..to make your immune system STRONG..to avoid attacks of any virus.GROW UP at least after facing this Corona..Until vaccine gets invented.'
b'RT @RashadAdeel: @betterpakistan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all\xe2\x80\xa6'
b'@CNN QUIT all your GOOD habits of Smoking, Alcohol, Drug, PORN, Premarital Sex/Extramarital Affair..to make yourself mentally &amp; physically healthy..to make your immune system STRONG..to avoid attacks of any virus.GROW-UP at least after facing this Corona..Until vaccine gets invented'
b'@CNN QUIT all your GOOD habits of Smoking, Alcohol, Drug, PORN, Premarital Sex/Extramarital Affair..to make yourself mentally &amp; physically healthy..to make your immune system STRONG..to avoid attacks of any virus.GROW UP at least after facing this Corona..Until vaccine gets invented'
b'@Shafqat_Mahmood @DrMuradPTI please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down. https://t.co/QWD0WcJITg'
b'RT @Satyendra_UP72: He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which no muslim like becoz their\xe2\x80\xa6'
b'Thank you @Bob_Wachter for a scientifically sound overview of where we are at in the Bay Area / SF with regards to the corona virus. Following you has helped me make sense of this crazy pandemic. Hope you can relax a little this thanksgiving week, you deserve it! \xf0\x9f\x99\x8f\xf0\x9f\x8f\xbd https://t.co/OObcmSkviQ'
b"Corona virus doesn't choose people, Corona reveals the malicious behavior of good citizens. be Nice..."
b'RT @b_scrino: @2020predicts @Louis_Tomlinson @LiamPayne Lost my dad to Corona VirusLeaving my 12 year old brother suffering from cancer in\xe2\x80\xa6'
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b'Seasonal Flu kills about 3,500 Americans under age of 45 ever year and to date we had about 4,500 Americans under age of 45 who died from Corona Virus. All those 3,500 Seasonal Flu Deaths just a Big A Tragedy as 4,500 Corona Virus Deaths and yet no one ever says word about Flu! https://t.co/86MSpF8ljT'
b'RT @AnandiChetna: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https://\xe2\x80\xa6'
b'RT @saurabhpandeyc1: #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80He is afraid of nationalism and loves terrorismNationalism implies loyalty to nation which\xe2\x80\xa6'
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b'#Shutdownallinstitutions It is not seasonal flu it is CORONA virus'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'@PTIofficial @imrankhan_TI ASLAM-O-ALIKUM. I come here to say that there we got 2 cases of corona virus in THE CITY MODEL SECONDARY SCHOOL so pls will this school'
b"@JJHantsch @FoxNews You take credit for everything then. 250k death, Voter suppression, Corona virus response and the vaccine...you can't just select what to praise him for. How fuc*ing convenient?"
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Opposition is Accomplice in Mass Spreading of Corona Virus As All Damage From Corona Virus Will Lie o\xe2\x80\xa6'
b'Saudi Arabia hosts the #G20 emergency summit session on NOV 21 due to Corona virus. This summit will be so helpful to charge our abilities and stop the virus \xf0\x9f\x91\x8f\xf0\x9f\x8f\xbb. #G20SaudiArabia https://t.co/gG5hu9zz0O'
b'heather corona virus 1'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'162 new cases of corona virus infection in Noida, one\xc2\xa0dead https://t.co/cp5rh5g1CS'
b"I'm corona virus"
b'@DonaldJTrumpJr  How does that "fake" Corona virus feel dumbshit'
b'@MBKBDK @cleopatraorly @MagaliOya @MachM6 @Josh48200313 I don\xe2\x80\x99t think his handling covid has been that bad tbh, he closed off China while Nancy Pelosi was dancing in China town saying the corona virus was fake and 2 months later she\xe2\x80\x99s ranting on him for his a handling, yes he did down play it but he needed to try and save the economy'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PDM and Corona Virus Agree to Work Together in Pakistan As Both Agree For Mass Spreading of Corona Pa\xe2\x80\xa6'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @laila19B: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Khyber Pakhtunkhwa Government has cancelled Rashakai Jalsa as per the directions of PM Imran Khan to con\xe2\x80\xa6'
b'@ericbolling What about Elon Musk who, it turns out did 4 consecutive tests of which 2 showed positive. He has had half the corona virus according to the test results.'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b'@ProtecttheFaith  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'@NiallMcConnell5  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'@en_volve I believe the Corona Virus was something cooked up by the Dems and China to scare people and to see how willing we are going to follow'
b'@realDonaldTrump Good for you! But what about the hundreds of thousands of american people who have died of the new corona-virus? Hope you start caring about them #careforamericans'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 It's The Responsibility of All Political Parties to Show Restraint from Holding Jalsa and Public Gat\xe2\x80\xa6"
b'@DavQuinn  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'#tshirt Corona Virus With mask Hoodie https://t.co/SeTZq2H2XV https://t.co/Zp0JYgP2Y5'
b'@TapLHarV Well aids and hiv are more deadly than corona virus???????'
b'RT @AnandiChetna: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https://\xe2\x80\xa6'
b'@Victoriamary Van is one of the most magnificent artists! Its sad to see the amount of bad press he gets, particularly lately over his controversial corona virus views.'
b'PDM Peshawar rally: Illegitimate govt itself is a big corona@MoulanaOfficial Time to stop politicizing this virus.'
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'Is 5G The CAUSE of CORONA VIRUS? https://t.co/d5iw8EbU8Z via @YouTube'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b"@Yates19703 @RepStefanik Pro life women who don't wear masks to prevent the spread of Corona Virus. In the 60's Pro Life people supported dropping bombs on civilians and the Death Penalty. That always confused me. How bout you?"
b'@velocirapture23 @LoraiTiffany @1socrfan @JamesWoods84 @HillaryClinton This is not a flu virus. It is a novel corona virus. This means it is new, and scientists have had to figure it out. We had no resistance, and herd immunity would not be feasible (before you start that course).'
b'RT @TheEmployYenta: Past VP Mike Pence aka the new figure on the Cream of Wheat box and Head of Trump\xe2\x80\x99s Corona Task force campaigns instead\xe2\x80\xa6'
b'@breeadail  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'@kennedyhall  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b"Wonder why their isn't any claim for false ads on TV regarding be it dishwsher, cloths, floor cleaner who is claiming that their products kill Corona virus. #COVID19India #COVIDIOTS"
b'@DrMuradPTI In schools students come from different families. In schools Corona virus can spread from one student to many students.... If we take a rest for two months that is not big matter... Safety is very important... Please close all educational institutes.....'
b'RT @Deshysmalls: The scariest thing about this Corona Virus is that you being careful is not enough, because your survival also depends on\xe2\x80\xa6'
b'RT @Cheech_1017: I dont wish Corona Virus on ANYONE but Donald Trump Jr. This is just straight KARMA ! Must be convenient to get emergency\xe2\x80\xa6'
b'@TaylorRMarshall  this a must watch regarding the Corona Virus, please give it your time \xf0\x9f\x99\x8f https://t.co/d9r6PnyWYn'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4You Can Counter Corona Virus by Only Following Govt SOPs as No One Can Save You From this Pandemic as\xe2\x80\xa6'
b'@DonaldJTrumpJr i hope you dont make it out if your corona virus! You are one corrupted and wicked creature! You are a waste of human skin !!!'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'The Government on Saturday informed that 608 new positive cases of novel Corona virus (COVID-19), 311 from Jammu division and 297 from Kashmir division, have been reported today thus taking the total number of positive cases in Jammu and Kashmir https://t.co/0yzyCkxUN3 https://t.co/326mDYxWSB'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'The Government on Saturday informed that 608 new positive cases of novel Corona virus (COVID-19), 311 from Jammu division and 297 from Kashmir division, have been reported today thus taking the total number of positive cases in Jammu and Kashmir https://t.co/pzHM3qc5MA https://t.co/dPQQOpY21r'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'@realDonaldTrump Donald trump is like corona virus it wont just leave the white house as well pack your bags up Donnie time for you to go stop dragging the inevitable out and leave with what LITTLE dignity you have left !!! https://t.co/xSAwoQa7Ub'
b'RT @RashadAdeel: @ImranKhanPTI please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all o\xe2\x80\xa6'
b'RT @REDBOXINDIA: Corona virus update India Nov20Total cases:9050213Active cases:439871Recovered:8475213Total Deaths: 132646New cases t\xe2\x80\xa6'
b'Idk why but mfs in nyc still don\xe2\x80\x99t wear masks in public areas then wanna be like HUH? When you tell them where yo mask at??? BITCH CORONA VIRUS IS REAL'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b"RT @shivandroid: @HogDexter @neurion92 @BRIMDELLA @KamalaHarris Flu is caused by influenza A, B. Corona virus is cause by SARS-CoV-2. They'\xe2\x80\xa6"
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b"@HogDexter @neurion92 @BRIMDELLA @KamalaHarris Flu is caused by influenza A, B. Corona virus is cause by SARS-CoV-2. They're different. Covid-19 is estimated 10x more lethal than flu, even at 1-2% mortality rate."
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'@VizierOpLinks BLM, antifa, KOZP are excemt from catching Corona virus internationally it seems.'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'@SenMikeShirkey so basiclly trump dished out corona virus relife in hopes you might undermine the will of the people'
b"@Pontifex  : Only you, Pope Francis, have been given the authority and ability to abate the Corona virus now plaguing the world. Corona warns of what is yet to come..So, when will you and all the bishops consecrate Russia to Mary's Immaculate Heart, as she requested in 1929?"
b'@ALT_uscis @GeraldoRivera I still say if he\xe2\x80\x99s so desperate to have something named after him then rename the Corona virus The Trump Virus.'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @Fantasy_lady21: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 Corona virus is   increasing day by day across the Country but the PDM Parties prefer politics ov\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @lionsofmirzapur: @shafqat_mahmood The Fuji foundation university closed a week ago due to corona cases We cannot risk the exposure of\xe2\x80\xa6'
b'@DavidCornDC 72 million Americans thought the corona virus would vanish after the Election in November.'
b"@MobileLegendsOL Id: 434583388Ign: corona virusHope you can notice me moonton I've been wanting to have King of Muay Thai but sadly it the past double 11 event i can't join due to some instances"
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'@ImAsoul255490 The European Union appeared for what it was at the beginning of the Corona virus crisis, so it appeared fragile and weak'
b"E be like sey Corona virus no dey kd, what in the world is this chunkus without facemask I'm seeing????? https://t.co/AXv8NsOICp"
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @TheMedicaIShort: Father can\xe2\x80\x99t touch his little baby as he is infected with the Corona virus... The baby\xe2\x80\x99s face tho.. \xf0\x9f\x98\xa2 https://t.co/0\xe2\x80\xa6'
b'@Qstang2 lol "whats the discussion?" what a dumbass. SCIENCE SHOWS WEARING A CLOTH/SURGICAL MASK DOES NOT STOP THE SPREAD OF CORONA VIRUS YOU FCKING MORON. I\'m not going to breathe bad air bc you fcking morons want to continue your covid theatre.'
b'@VaushV There\xe2\x80\x99s no way! Joe has a cure! He is going to do amazing things! He will cure racism. World poverty. Corona virus and so much more! He said he would!'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'@mike_wanaoni @DonaldJTrumpJr If you think any of this is happening, please find more to do with your life. None of it is important. There is no new Hitler. Corona virus will pass. Biden is president, and politics is boring again. No need to pee in your skinny jeans.'
b'@KyleKulinski If thats what corona wants, thats will it will take. And if not, another virus will emerge...whether natural or man-made.  Earth is over populated'
b'A coworker of mine really believes that they made up the corona virus to cover up people getting sick from new 5G towers \xf0\x9f\xa4\xa3'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @Fantasy_lady21: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 Corona virus is   increasing day by day across the Country but the PDM Parties prefer politics ov\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'Corona virus is still existing and it has its own impact like HIV , Hepatitis etc so necessary precautions are to be applied in daily living.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'The death of doctor, Muhammad Yassin from the city of #Darat_Izza, as a result of infection with the Corona virus.#COVID19 #\xd8\xaf\xd8\xa7\xd8\xb1\xd8\xa9_\xd8\xb9\xd8\xb2\xd8\xa9#\xd8\xaf\xd8\xa7\xd8\xb1\xd8\xa9\xd8\xb9\xd8\xb2\xd8\xa9#Aleppo#SyriaVia .@Anas_Alhaje https://t.co/rsJ8vS1swR'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b'RT @corvowine: Sorry to hear that Donny Jr.And his girlfriend has the "corona VIRUS,If anyone who knows them personally get them a messag\xe2\x80\xa6'
b"@2ubair_khan SOPs CANNOT be followed. It's useless. We have gone to uni after corona... there's no point of following SOPs in universities. No matter how hard one tries there are still 90% chances of transmission of virus"
b'RT @DrAnthony: Employers shun testing due to cost https://t.co/Gn0dLxuLnv #Saturday #SaturdayMorning #SaturdayVibes #Careers #Job #work #bu\xe2\x80\xa6'
b'RT @JibbyD: You know... if you are posting about how concerned you are about Khadim Rizvi\xe2\x80\x99s funeral being a super spreader, but are complet\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Corona Virus Prevention RecommendationsTo boost immune resilience-stress reduction. When the body is experiencing stress and holding onto it, the immune system will get affected. It\xe2\x80\x99s a natural reaction. Read more about how to reduce stress...https://t.co/HvM4PgwCgt https://t.co/fEObEX5vcO'
b'RT @rohini_sgh: Another nonsensical decision. Corona doesn\xe2\x80\x99t strike at night. Govts should instead be looking at strictly implementing wear\xe2\x80\xa6'
b'RT @BillFriar: @RandyRainbow BREAKING NEWS: Corona Virus is now reporting that it is HIGH, really fucking HIGH on Cocaine since it came int\xe2\x80\xa6'
b'Employers shun testing due to cost https://t.co/Gn0dLxuLnv #Saturday #SaturdayMorning #SaturdayVibes #Careers #Job #work #business #HumanResources #COVID19 #Corona #pandemic #pandemia'
b'Raider Nation Athletic Dept Corona #Virus Video \xe2\x80\x93 YouTube https://t.co/EoqzvIpCaLhttps://t.co/LHWLnwJKt5#AceUnderhill #AllSportsMarket #ASM #BernieNicholls #Biden #China #ChrisRabalais #Christmas #DraftKings #Harris #Hollywood #IndependenceDay...'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Current Conditions for #Sayre PATemp: 47.6FWind Chill: 47.6FHumidity: 78%Dew Point: 41.1F Barometer: 30.484 inHgWind: 1 mph from the NNECorona Virus Weekly Stats:Cases: 291.000000Deaths: 5.000000Survival: 98.000000#weewx #nepa #bradfordcounty'
b'RT @pregNancyDrew_: Asked my mother to draw sun. She drew the Corona virus instead https://t.co/ZxQiudVcRR'
b'@betterpakistan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'RT @RashadAdeel: #Shutdownallinstitutions please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test\xe2\x80\xa6'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b"@DrKumarVishwas I am a Research Scientist-well it's a battle of Species to rule the World. Even if China has invented the Corona Covid-19 virus as a Biological warfare to be World No. 1, why we are not hearing anymore about China's Corona deaths ?Means they have the treatment or vaccine for it. https://t.co/f4FgFE3GxG"
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'I wonder if there\xe2\x80\x99s corona virus in Bar\xc3\xa9in? \xf0\x9f\xa4\x94'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'@BillKristol Just like the Corona Virus was a Hoax!!!'
b'Salam. The corona virus situation in our country is highly deadly. The positivity ratio had inclined by 40 percent and the death percentage by 180 percent. In this situation, there a dire need to close all educational institutions as soon as possible.'
b"RT @FXdestination: The risk of taking the globalists' gene-altering Corona 'vaccine', tested for only a few MONTHS, is far higher than the\xe2\x80\xa6"
b'@theadrianmolina Yes...the love Corona virus has for attacking your lungs \xf0\x9f\x92\x98'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@klausenhus They are literally doing nothing on corona virus anymore. But all the food is Mexican and the people actually like each other save the fringes. I do miss it. Where do x you live?'
b'@FoxNews typo. Did u mean \xe2\x80\x9c.....takes credit for corona virus development, says Americans wouldn\xe2\x80\x99t have one yet without his leadership\xe2\x80\x9d'
b'#Shutdownallinstitutions please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'if you have Corona virus check your karma.'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4The Daily Rise of Corona Virus Graph in Pakistan is An Alarming Situation &amp; If Opposition Did Not Sho\xe2\x80\xa6'
b'RT @CookCntyCourt: November 20, 2020 Update on Court Operations and the Coronavirus:https://t.co/Cd4ikd9ARv'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @CMOGuj: Gujarat Govt decides to postpone the reopening of schools and colleges in Gujarat from November 23 in the wake of the current C\xe2\x80\xa6'
b"@biannagolodryga Our corona response has been a near total failure of National strategy &amp; policy. Despite Herculean efforts by a few, each state was mostly forced to fight this on their own.The virus doesn't care about state boundaries.100 years on, our response will still be a sad case study"
b'RT @TFP_Tauseef: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4All eyes were on the battle between the parties in the political arena, while on the other hand, the\xe2\x80\xa6'
b'Staggering Corona virus cases have now soared past 12 million. New daily cases are approaching 200,000: on Friday, the country recorded more than 198,500, a record.'
b'RT @sanjeevpunj71: Are MAHE authorities ready take full responsibility of keeping students safe from contracting Corona virus. Do you have\xe2\x80\xa6'
b'@SkyNews @rtenews @BBCNews@cnnbrk @VirginMediaNews @ABC@Channel4News @UN @EU_Commission @Europarl_EN@POTUS @realDonaldTrump @CBCNews @LeoVaradkar @BorisJohnson @MichealMartinTD@CanadianPM @JoeBidenIn regard to Corona Virus Vaccine!Better Put in this tweet! https://t.co/cPblQ4olkz'
b'RT @ashokgehlot51: In this battle against #corona, a mask is considered as good as a vaccine until we have a vaccine against the virus. Con\xe2\x80\xa6'
b'Sir corona cases r increasing day by day, most of the students r infecting with virus , no one is following SOPs. Please take serious steps to tackle corona otherwise precious lives will no longer remain. Health should be first priority. #Shutdownallinstitutions @Shafqat_Mahmood https://t.co/FRs8nqcDv8'
b'RT @PincheeeVanessa: We\xe2\x80\x99re gonna lose 2021 to COVID the way we lost 2020. All we can hope is that the Biden corona virus task force will sh\xe2\x80\xa6'
b'@realDonaldTrump Hey, now that your son has Corona virus what are you going to do, I think I will go play golf or eat a hamburger.'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Whole World Appreciated Pakistan Efforts to Control Corona Virus and it's Our Duty to Contain This Vi\xe2\x80\xa6"
b'@DineshDSouza The original "Corona virus"'
b'RT @pregNancyDrew_: Asked my mother to draw sun. She drew the Corona virus instead https://t.co/ZxQiudVcRR'
b'@Tara61711 I agree with lockdowns I lost my brother today corona virus \xf0\x9f\x98\xa2'
b'@globaltimesnews These countries are giving you the corona virus back along with a piece of meat. You should be happy.'
b'Donald Trump failure to combat the Corona virus has not only been deadly but if you look at this chart.. How devastatingly sad that we, the greatest country supposedly on Earth have failed so dramatically. https://t.co/3R0vMPnapX'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b"One good thing about 2020 and the Corona Virus.... No Jehovah's Witnesses have knocked on our door..."
b'@thehill @TheHillOpinion A state worst hit by the Corona virus... and this has what she has to say? Pathetic.'
b'@DrMuradPTI sir! Corona virus is on his peak the schools are not following sops due to current situation  health of students are in great danger please close all schools and colleges on 24 November 2020 #Tuesday for our healths! https://t.co/y72qvjQ8Gm https://t.co/NjSyAPxcN3'
b'@CandianDuck @bdomenech @EliseStefanik Seriously, are you out of touch? Trump has been very verbal since the corona virus reared it\xe2\x80\x99s head about the cure. Working daily with multiple people,groups,scientists,doctors while Biden stayed in the basement!'
b'RT @_Mansoormalik: Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of stude\xe2\x80\xa6'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b'Corona virus is no joke government should be serious and close schools as fast as they can it can save millions of students lives THANK YOU@DrMuradPTI @Shafqat_Mahmood #Shutdownallinstitutions #CloseSchoolsNOW #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4'
b'Civil unrest in the US ensues. Not because of the corona virus but it doesn\xe2\x80\x99t help. The general population is extremely confused. What is going on. The stock market recovers. Cases start to drop. School starts. Things are looking up.'
b'Are MAHE authorities ready take full responsibility of keeping students safe from contracting Corona virus. Do you have sufficient medical arrangements to provide medical facilities for all kids in case the Crona virus spread among students.'
b'@Charleekes @EmekaJOgbu1 @GovernorIkpeazu @GhenhisKhan Your idol contracted corona virus and went to an Isolation center in Lagos. He knew he had nothing on ground in his state for treatment and he ran to Lagos. This is the fellow you are defending, shameful!'
b'RT @abdulah18150193: We are not afraid of TestBut we are afraid of Corona virus#coronarisedelaymcat #DelayMdcat'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b"It doesn't take a Rhodes Scholar to see Corona Virus BAD and getting WORSE in America and that's because lots of Americans not taking it seriously and for most...Corona Virus Survival Rate 99.87% now...they will be fine but Tens of Thousands Americans going die needlessly #Truth https://t.co/iqBFt19bBQ https://t.co/xNIwNOpNz9"
b'RT @pregNancyDrew_: Asked my mother to draw sun. She drew the Corona virus instead https://t.co/ZxQiudVcRR'
b'RT @Noorehhhhh: TrueCases of Corona virus are increasing day by day, our lives matter#Shutdownallinstitutions@Shafqat_Mahmood@ImranKhan\xe2\x80\xa6'
b'RT @AlisonBlunt: 1) Quote thread"Thanks to \'Corona\', many people now understand how the PCR test works &amp; will be even better able to under\xe2\x80\xa6'
b'RT @mona_fawaz: The only pollution on the scene is the freakin noise of the police force telling people to leave the Corniche when every st\xe2\x80\xa6'
b'RT @NerddStark: corona virus hearing that school is resuming #ASUU https://t.co/9ro70ODxGA'
b'RT @amarbail1: I believe we never controlled the spread of corona even earlier because it was rightly said high temperature can suppress th\xe2\x80\xa6'
b"RT @FXdestination: Ask yourself:Why would all of the governments pushing the fake 'Corona crisis' be hell-bent on injecting everyone with\xe2\x80\xa6"
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@TheUSASingers @mad4clark More fitting to call this negligent wave of corona~ The Trump Virus.'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PM Imran Khan Took Important Decision and Ban All Rallies and Jalsa As He Make Him Example For Other\xe2\x80\xa6'
b'Met a guy who believes Corona Death are not really because of the virus but caused by fear of Corona. Goes on telling a conspiracy theory which was shared on SM as his own vision'
b'@DOMMUNACHIDIE @vanguardngrnews Corona virus still dey...'
b'RT @cstudvill: Gm Wake Tf Up And Smile &amp; Gett Dress Grab Da Bleach Bottle /Gloves/ Mask And Lettz Fight Diz \xe2\x80\x9cCorona Virus\xe2\x80\x9d \xf0\x9f\xa6\xa0 Man Da Rona Ha\xe2\x80\xa6'
b"@DrMuradPTI @Shafqat_MahmoodTake corona virus serious even the sops aren't able to stop the spread of the virus you are playing with the health of millions of  students #Shutdownallinstitutions"
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'RT @kavita_tewari: Molvi Khadim Hussain Rizvi, who demanded nuclear attack on France for Prophet Mohammad cartoons died of Corona Virus in\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4PDM and Corona Virus Agree to Work Together in Pakistan As Both Agree For Mass Spreading of Corona Pa\xe2\x80\xa6'
b"RT @PotashAlum_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 Don't play with the lives of children close  Educational institutes to control corona virus@Team4Pa\xe2\x80\xa6"
b'@unrivaled_psu @ObligatoryPSU @buchignani This is so stupid, you can believe in Corona Virus and also realize that it will have a very small impact on a college kid'
b'I slick want to go to Atlanta but Corona virus \xf0\x9f\xa5\xb4'
b'Preventing pandemic and expanding personalized healthcare was an opportunity that Saudi Arabia saw with Corona virus. #G20SaudiArabi https://t.co/jVaY3yzXPc'
b'RT @cricket_wars: In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing with the lives\xe2\x80\xa6'
b'RT @aishahk8_: Don\xe2\x80\x99t you dare do worthless processions and spread corona virus in my city! This crap plot to infect and kill citizens shoul\xe2\x80\xa6'
b'Although of the huge affects that caused by the Corona Virus on the G20 economies, but the Saudi presidency not only focused on avoiding the #G20 economies the impact of the pandemic, but even care of the human and supporting the developing countries #G20SaudiArabia https://t.co/QA8QafxkM6'
b'Does the Mormon \xe2\x80\x9cprophet\xe2\x80\x9d think that gratitude will make the corona virus go away? Solve the problems of Black Americans who fear police interactions? This isn\xe2\x80\x99t about healing, this is about marketing. Fuck off Nelson.'
b'RT @JibbyD: You know... if you are posting about how concerned you are about Khadim Rizvi\xe2\x80\x99s funeral being a super spreader, but are complet\xe2\x80\xa6'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'RT @MwalimChurchill: Bobi wine was charged with spreading corona virus \xf0\x9f\xa4\x94..Comedy is a stress reliever..!!'
b'@Dr_YasminRashid please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @CEO_AISOMA: We must not be afraid of the virus. Rather, we must actively fight it from all angles and bring it to its knees.~ Murat#C\xe2\x80\xa6'
b'3924779 people recovered from Corona today. Total Corona virus recoveries: 39580677   Source: WHO Situation Reports  #COVID19 #coronavirus #StaySafe'
b"Trump and Pence could of made the corona virus a lot less with out there lies.But instead let's work on the election  and 255000 americans died.They said it is what it is.SHAMEFUL"
b'RT @MiteiRober: Breaking : Donald Trump Jr who tested positive for corona virus  has said he will pass time in isolation cleaning his guns.'
b'@thehill Yes.Corona Virus Deaths = 260,427  #TrumpDeathTollNational Debt = $27,246,599,172,457.42 #NationalDebthttps://t.co/m2EPDL6gNE'
b'Do your part, wear a mask. Continue social distancing and washing your hands for at least 20 seconds. Avoid big Thansgiving get togethers next week by limiting how many are in attendance. We need to get the Corona Virus under control before it causes the Apocalypse https://t.co/UKgR3Lwzs0'
b'@DrMuradPTI We Want Education not Lockdown, Please Keep schools open. There is nothing like Corona Virus. Let us Study.'
b'RT @Noorehhhhh: TrueCases of Corona virus are increasing day by day, our lives matter#Shutdownallinstitutions@Shafqat_Mahmood@ImranKhan\xe2\x80\xa6'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'No, I don\xe2\x80\x99t want to visit my family. Corona virus is raging, I HAD IT, so you shouldn\xe2\x80\x99t want to visit yours either. My family has never respected me or my dietary restrictions / issues and I know my mans family won\xe2\x80\x99t either. So I\xe2\x80\x99m supposed to waste my time and gas money ?? Bitch'
b'TrueCases of Corona virus are increasing day by day, our lives matter#Shutdownallinstitutions@Shafqat_Mahmood@ImranKhanPTI@DrMuradPTI https://t.co/blbLsWzW5a'
b'NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.@Shafqat_Mahmood @DrMuradPTI @Asad_Umar @betterpakistan https://t.co/HMzuNJJtgA'
b'RT @pregNancyDrew_: Asked my mother to draw sun. She drew the Corona virus instead https://t.co/ZxQiudVcRR'
b'@KTRTRS Hi Mr. You are also Following Double standards..say corona virus 2nd wave is going on &amp; need to follow norms at one end.For ur political speeches.. huge public gathering u r playing with public health at another end.'
b'No waste should be burned in Delhi , Pollution and Corona virus spreads like wildfire. https://t.co/2pRw7LaHJX'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'Sharing is Caring.  Look and Learn.  Corona Virus is the Fake News #KBF https://t.co/6WaK2uWBDb'
b'@Shafqat_Mahmood (part 1) please read this and think ahout the students future. Corona virus is increasing day by day yet our schools are not closing https://t.co/lmjdWVAT3A'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b"@EricDSnider MY NEIGHBOR'S DOG TOLD ME THAT OBAMA PUT THE VIRUS IN THE CORONA AND THE AUTISM IN THE VACCINES!!!!!!!!?"
b'CORONA IS A MAN MADE VIRUS DESIGNED TO KILL PEOPLE....... https://t.co/1BcLH7FtAi'
b'RT @aishahk8_: Don\xe2\x80\x99t you dare do worthless processions and spread corona virus in my city! This crap plot to infect and kill citizens shoul\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @lassiter_wes: When society values the economy more than human lives it doesn\xe2\x80\x99t need a virus for we are already sick. #Corona'
b'RT @hloveharoon: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly pla\xe2\x80\xa6'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@trspartyonline @KTRTRS @mkrkkpmla @puvvada_ajay Where is corona virus \xf0\x9f\x98\x82\xf0\x9f\x98\x82'
b'What awful name will the drug companies give the Corona virus vaccine? Covidata? Coronizzi? Cova McCovface? I have to know what to ask my doctor about from the commercial'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'@betterpakistan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b'The President\xe2\x80\x99s Corona Virus Task Force Says the Cavalry is Coming Due to Donald Trump; Did Pfizer Act to Throw the Election? https://t.co/aJpBJry7aI'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@betterpakistan please look into the NMDCAT being held on 29th November. 2 lac students are appearing in the test from all over PK with at least 5000 students in one centre, it will cause a huge spread of corona virus. The test should be delayed until cases go down.'
b"Trump can't accept he lose on elections patronizing corona virus on the other hand. Not only that he lose his brother Robert Trump on Chinese virus a.k.a lethal injection &amp; poisoning. Love fine humor,commander !"
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'Breaking : Donald Trump Jr who tested positive for corona virus  has said he will pass time in isolation cleaning his guns.'
b'RT @SteveSchmidtSES: Corona virus task force because he is incompetent. He was an incompetent Governor who remains manifestly hostile to sc\xe2\x80\xa6'
b'@JimKotowski @mchooyah Haha.  Another clown ignoring the Corona virus and democrats locking down their states/cities and ruining the economy'
b'RT @JibbyD: You know... if you are posting about how concerned you are about Khadim Rizvi\xe2\x80\x99s funeral being a super spreader, but are complet\xe2\x80\xa6'
b'RT @Thomas_Binder: @HegKong As a doctor I state here and now that there is absolutely no indication for a vaccine against a corona common c\xe2\x80\xa6'
b'@MeghanMcCain So what should trumpGet for the deaths of the corona virus? And yes, I\xe2\x80\x99m a veteran. I respect your father but you didn\xe2\x80\x99t care what trump said about your dad. I question your loyalty.'
b'This explains the Trump administration\xe2\x80\x99s view on the corona virus in a nut shell. https://t.co/0qZIwuB7Dm'
b'@DuxQ_ @oloye__ Schools that were closed due to the corona virus?'
b'@DrMuradPTI Educational institutes have become the hub of corona virus .. literally'
b'RT @amitanatverlal: After completing one year, the virus must be like "koi mujhe happy birthday wish Corona".'
b'@ZeeNews @narendramodi Hamid Ansari is the faithfull brother of Corona virus.'
b'@SenKamalaHarris Shut up wow. Ive had the corona virus. Ive had the flu worse then that shit.'
b'RT @Marco_Acortes: Corona virus....its coming'
b'Amazing video by our police force to fight Corona Virus please do watch the video and share it to others to https://t.co/PLuwCKKtK4'
b'RT @AhsanBu44106078: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed and what#PDM is doing they are constantly p\xe2\x80\xa6'
b'@SenMikeShirkey Absolutely nobody is stupid enough to believe that this was just about corona virus lol. Trump himself is now saying that\xe2\x80\x99s wrong. Doesn\xe2\x80\x99t matter tho, Georgia had the courage to stand up to Trump.'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @PincheeeVanessa: We\xe2\x80\x99re gonna lose 2021 to COVID the way we lost 2020. All we can hope is that the Biden corona virus task force will sh\xe2\x80\xa6'
b'RT @pregNancyDrew_: Asked my mother to draw sun. She drew the Corona virus instead https://t.co/ZxQiudVcRR'
b'@realDonaldTrump Talk corona virus plz you big dummy'
b'what\xe2\x80\x99s not corona virus but feels like corona virus https://t.co/V04VlZolIx'
b"RT @MRKalmati1: Let's go to Peshawar No one's father can stop this caravan now. If you can stop, stop, but remember that whatever comes to\xe2\x80\xa6"
b"@WIONews It's amazing considering the number of deaths due to corona virus in USA."
b"RT @PotashAlum_: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4 Don't play with the lives of children close  Educational institutes to control corona virus@Team4Pa\xe2\x80\xa6"
b'RT @lassiter_wes: When society values the economy more than human lives it doesn\xe2\x80\x99t need a virus for we are already sick. #Corona'
b'HIPAA rules enforcement for current intensional falsification of regular fly symptoms as a \xe2\x80\x9ccorona virus\xe2\x80\x9d diagnosis I order to generate triple profit.  https://t.co/jclMmSqz5o'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @lassiter_wes: When society values the economy more than human lives it doesn\xe2\x80\x99t need a virus for we are already sick. #Corona'
b'RT @coastal_eddyLB: Corona Virus explained in craft terms: you and 9 friends are crafting. 1 is using glitter. How many projects have glitt\xe2\x80\xa6'
b'RT @U_S786: ##\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playing\xe2\x80\xa6'
b'I told my mother-in-law that computer viruses are related variances to the Sars-Corona virus, so she steers clear of my "sick" computer.'
b'Remember the part of quarantine where we\xe2\x80\x99re all just saying \xe2\x80\x9ccorona virus\xe2\x80\x9d around the house in different voices'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'RT @DanishJui: Information Minister @shiblifaraz said FIR will be registered against opposition leaders and organizers of the #PDMPeshawarJ\xe2\x80\xa6'
b'RT @muhamma93936801: #DelayMdcat The test must not be conducted in this situation.Corona Virus spreading rapidly.\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f@MJibranNasir'
b'Total deaths: one measure of the intensity of the SARS 2 Corona Virus pandemic in BC.'
b'RT @RealMMyers78: If corona virus kills Laurie before I do, I\xe2\x80\x99m gonna be sooo pissed.'
b"RT @FXdestination: Ask yourself:Why would all of the governments pushing the fake 'Corona crisis' be hell-bent on injecting everyone with\xe2\x80\xa6"
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'RT @dril: if you can smell your own balls that means you have corona virus . bad news for all you Stupid mother fuckers on here'
b'@hinaparvezbutt BASHARAAM &amp; Bagaaraatuoo I mean GHQ Gens &amp; PTI selected think themselves immortal &amp; above than all reach including Corona virus \xf0\x9f\xa6\xa0 but always ready to surrender infront of India and west'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'RT @Bisma_PAK: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4In second wave of corona virus more caution is needed  and what #PDM is doing they are constantly playi\xe2\x80\xa6'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'What a calm in Market..even bad news pouring from corona virusLast Feb20 China only having virus and market was calm..and on fear it will spread to world ,market tank in March20Now whole world has virusmajor player ready to play by DEC end when market all time high.\xf0\x9f\x90\xbb\xf0\x9f\x90\xbb\xf0\x9f\x90\xbb'
b'RT @mochiibangncub: I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hm\xe2\x80\xa6'
b'RT @matanevenoff: China has used the #coronavirus to take advantage of the world, especially #HongKong to stop the protests there. The #Hon\xe2\x80\xa6'
b'I really hope the corona virus goes away soon so we can meet soon\xf0\x9f\xa5\xba\xf0\x9f\x98\xad#\xea\xb2\xbd\xec\xb6\x95_\xec\x84\x9c\xec\x9d\xb4\xec\x82\xac\xeb\x8b\x98_\xed\x83\x84\xec\x8b\xa0\xec\x9d\xbc#EUNKWANG_SUNSHINE_DAY https://t.co/hmFRwNgOap'
b'#DelayMdcat The test must not be conducted in this situation.Corona Virus spreading rapidly.\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f\xf0\x9f\x99\x8f@MJibranNasir'
b'RT @AnandiChetna: Fear of nationalism !"Nationalism is more dangerous than Corona virus" ~ Hameed Ansari Shame on #\xe0\xa4\xb9\xe0\xa4\xbe\xe0\xa4\xae\xe0\xa4\xbf\xe0\xa4\xa6\xe0\xa4\x85\xe0\xa4\x82\xe0\xa4\xb8\xe0\xa4\xbe\xe0\xa4\xb0\xe0\xa5\x80 https://\xe2\x80\xa6'
b'@TonyDElia_ John 1:1 - Exodus 23:20-21 &amp; Deuteronomy 31:26.  Why did they call it "Corona Virus"?  What are they really trying to "vaccinate" against? Revelation 19:13'
b'RT @andy5_123: @DrLiMengYAN1 on the Lude media (1)From the emails of Ecohealth Alliance,scientists did not prove or even check where the C\xe2\x80\xa6'
b'RT @WMatire: The only numbers Trump should be counting right now are, The numbers of dead Americans, that continue to die under his watch f\xe2\x80\xa6'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4You Can Counter Corona Virus by Only Following Govt SOPs as No One Can Save You From this Pandemic as\xe2\x80\xa6'
b'N57,400 to take a corona virus test in Nigeria..  far more than the national minimum wage. @NCDCgov What is going on. You have turned this pandemic to a Business enterprise. Even when other countries are running free tests.'
b'@DrDenaGrayson @CDCgov @ClayTravis  Hey Clay Virus: Are you going to call @DrDenaGrayson a Corona Bro? #ClayVirus'
b'@d0rkph0enix i do not like corona virus and ham , i do not like it amias i am'
b'RT @ShanzayAhmd: #\xd8\xb3\xdb\x8c\xd8\xa7\xd8\xb3\xd8\xaa_\xd9\x86\xdb\x81\xdb\x8c\xda\xba_\xd8\xac\xd8\xa7\xd9\x86_\xd8\xa8\xda\x86\xd8\xa7\xd8\xa4Maulana Fazal-ur-Rehman is the Official Brand Ambassador of Corona Virus as He Will Spread This Virus\xe2\x80\xa6'
b'Hey @realDonaldTrump it seems  #BrianWilliams on the @11thHour had high praise for @GeraldoRivera concerning your leadership on the Corona Virus vaccine \xf0\x9f\x92\x89 \xf0\x9f\xa6\xa0 https://t.co/DeWZtAfoge'
   """
 
    custom_tokens = remove_noise(word_tokenize(custom_tweet))
 
    print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))
 
    ##tweets_list1 = tweets_list
 
    ##tweets_tokens = remove_noise(word_tokenize(tweets_list1))
 
    ##print(tweets_list1, classifier.classify(dict([token, True] for token in tweets_tokens)))
