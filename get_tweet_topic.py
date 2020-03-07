import re
import time
import pickle
import numpy as np
import tweepy
import gensim
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model

import db_queries
import status_streams
'''
code needed to retrieve the topic from a tweet
'''
nltk.download('punkt')
#set stopwords
nltk.download('stopwords')
stop_words = nltk.corpus.stopwords.words('english')
custom = ['?','(', ')', '.', '[', ']','!', '...', '-', '@', '->','https',
        ';', "`", "'", '"',',', ':', '*', '~' , '/', '//', '\\', '&', 'n', ':\\']
stop_words.extend(custom)


#prepare incoming tweets by removing twitter mentions, links, and emojis
#set all letters to lowercase
#remove stopwords and tokenize
def clean_status(raw_status):
    remove_mentions = re.sub(r'@[A-Za-z0-9]+', '', raw_status)
    remove_links = re.sub('https?://[A-Za-z0-9./]+', '', remove_mentions, flags=re.MULTILINE)
    remove_bitly_links = re.sub(r'bit.ly/\S+', '', remove_links)
    remove_non_ascii = re.sub(r'[^\x00-\x7F]+', '', remove_bitly_links)
    set_lowercase = remove_non_ascii.lower()
    token = word_tokenize(set_lowercase)
    filtered = [words for words in token if not words in stop_words]
    return filtered


#convert words to bigrams
def get_bigrams(words, bi_min=15, tri_min=10):
    bigram = gensim.models.Phrases(words, min_count=bi_min)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return bigram_mod


#use model to inference the topic of the tweet. return topic
def guess_topic(raw_status, model, corpus, classifier):
    test_vector_list = []
    scaler = StandardScaler()

    #clean raw status, get bigrams, and corpus
    status = clean_status(raw_status)
    bigram = get_bigrams(status)
    full_bigram = bigram[status]
    corpus = corpus.doc2bow(full_bigram)

    #grab saved model and topic vector
    top_topics = model.get_document_topics(corpus, minimum_probability=0.0)
    topic_vector = [top_topics[i][1] for i in range(15)]
    test_vector_list.append(topic_vector)

    #use topic vector and saved classifier to classify status
    #returns only the score
    x = np.array(test_vector_list)
    x_fit = scaler.fit_transform(x)
    prediction = classifier.predict(x_fit)
    score = top_topics[prediction[0]][1]
    return score

def guess_topic_pipeline(api, conn, model, corpus, classifier):

    while True:
        cursor = conn.cursor()
        db_queries.create_temp_tweets_table(cursor)
        conn.commit()

        #use pipeline to grab tweets off twitter
        print('Retrieving statuses from streams...')
        status_streams.streaming_pipeline(api, cursor)
        print('Done retrieving...')

        #grab tweets from table
        statuses = db_queries.read_raw_statuses(cursor)

        try:
            #iterate through each row, clean text, classify, and like the tweet using its id
            print('Iterating db for streams...')
            for row in statuses:
                current_status = row[1]
                score = guess_topic(current_status, model, corpus, classifier)
                if row[2] != 'True':
                    if score > 0.5:
                        api.create_favorite(row[0])
                        print('Just liked: ', current_status)
                        print('with score: ', score)

        except tweepy.TweepError as e:

            if e.api_code == 144:
                print(e)

        #drop temp table and close cursor
        print('Dropping the tempTweets table...')
        db_queries.drop_table(cursor, tempTweets)
        cursor.close()
        time.sleep(21600)
