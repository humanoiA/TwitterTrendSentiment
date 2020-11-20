from operator import itemgetter
import tweepy
import pickle
import re
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import string
from nltk import pos_tag,word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
lmtzr=WordNetLemmatizer()
CONSUMER_API_KEY='dy2pgvjoNagUwKCriCYQJZsDx'
CONSUMER_API_SECRET_KEY='ASYbSKjXbaXgGSK7PRGJpTzEBIjwZvfOqsS4TbZvDe2l334KpI'
ACCESS_TOKEN='739119495684317189-GBD2tIufe1FZYFE2ebxOLwkWUb7iWwI'
ACCESS_TOKEN_SECRET='MdpoliszyEvjxrHCSWJGwq6IfbL6qLkCGQfZ771q6oO4N'
auth = tweepy.OAuthHandler(CONSUMER_API_KEY, CONSUMER_API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
pd.set_option('display.max_colwidth', -1)
api = tweepy.API(auth)
def trends():
    data = api.trends_place(2282863, '#')
    trends = data[0]["trends"]
# Remove trends with no Tweet volume data
    trends = filter(itemgetter("tweet_volume"), trends)
# Alternatively, using 0 during sorting would work as well:
# sorted(trends, key=lambda trend: trend["tweet_volume"] or 0, reverse=True)
    sorted_trends = sorted(trends, key=itemgetter("tweet_volume"), reverse=True)
    #print(sorted_trends[:15])
    return sorted_trends[:10]
def get_sentiments(trend_name):
    infile=open('data.pkl','rb')
    model_NB=pickle.load(infile)
    listOfTweets=pd.Series()
    count=1
    for tweet in tweepy.Cursor(api.search,q="#"+trend_name,count=5,
                           lang="en",).items():
        if 'RT' in str(tweet.text):
            continue
        #print(tweet.text)
        count=count+1
        tweet_str=re.sub(r"(?:\@|https?\://)\S+", "", str(tweet.text))
        tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
        tweet_token=tokenizer.tokenize(tweet_str)
        for j in range(len(tweet_token)):
            for word, tag in pos_tag(word_tokenize(tweet_token[j].lower())):
                wntag = tag[0].lower()
                wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
                if not wntag:
                    lemma = word
                else:
                    lemma = lmtzr.lemmatize(word, wntag)
        #print(dummy_df.description[i][j])
            tweet_token[j]=lemma
        tweet_clean=" ".join(tweet_token)
        #print(tweet_clean)
        listOfTweets=listOfTweets.append(pd.Series(tweet_clean),ignore_index=True)
        if count==30:
            break
    listOfTweets.drop_duplicates(keep='first', inplace=True)
    print(listOfTweets)
    predictions=model_NB.predict(listOfTweets)
    predictionNum=Counter(predictions)
    return predictionNum[0]/(predictionNum[0]+predictionNum[4])
    #print(predictionNum[4]/(predictionNum[0]+predictionNum[4]))
#get_sentiments('Independence Day')
trends()