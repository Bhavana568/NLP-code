from nltk.tokenize import sent_tokenize, word_tokenize 
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer 
from extract_tweets import extraction

def processing():
    read_tweet1 = extraction()
    #print(read_tweet1)
    # remove url
    import re
    text = read_tweet1
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

    return t0