import tweepy
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import follow


'''
code needed to retrieve the topic from a tweet
'''


stop_words = nltk.corpus.stopwords.words('english')
custom = ['?','(', ')', '.', '[', ']','!', '...',
';',"`","'",'"',',', "'s", "'ll", 'ca', "n't", "'m", "'re", "'ve"]
stop_words.extend(custom)

#lemmatize, tokenize, and remove stopwords in a tweet
def prepare_tweet(tweet):

    filtered_tweet = []
    finished_tweet = []
    lowered_tweet = tweet.lower()
    tokenized_tweet = nltk.word.tokenize(lowered_tweet)

    for word in tokenized_tweet:
        lemmatized = WordNetLemmatizer().lemmatize(word, 'v')
        filtered_tweet.append(word)

    finished_tweet = [word for word in filtered_tweet if not word in stop_words]
    return finished_tweet


def get_topic(clean_text):

    asdf
