import re
import tweepy
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords

import follow

'''code needed to retrieve the topic from a tweet'''


stop_words = nltk.corpus.stopwords.words('english')
custom = ['?','(', ')', '.', '[', ']','!', '...',
';',"`","'",'"',',', "'s", "'ll", 'ca', "n't", "'m", "'re", "'ve"]
stop_words.extend(custom)

#prepare incoming tweets by removing twitter mentions, links, and emojis
#set all letters to lowercase
#remove stopwords, tokenize, and lemmatize tweets
def prepare_tweet(raw_data):

    remove_mentions = re.sub(r'@[A-Za-z0-9]+', '', raw_data)
    remove_links = re.sub('https?://[A-Za-z0-9./]+', '', remove_mentions, flags=re.MULTILINE)
    remove_bitly_links = re.sub(r'bit.ly/\S+', '', remove_links)
    remove_non_ascii = re.sub(r'[^\x00-\x7F]+',' ', remove_bitly_links)
    set_lowercase = remove_non_ascii.lower()
    tokenized = TweetTokenizer().tokenize(set_lowercase)
    remove_stopwords = [words for words in tokenized if not words in stop_words]
    lemmatized = [WordNetLemmatizer().lemmatize(word) for word in remove_stopwords]

    return lemmatized



#use model to inference the topic of the tweet. return topic
def guess_topic(clean_text):

    asdf
