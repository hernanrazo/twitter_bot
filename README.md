#Twitter Bot
This project is a twitter bot that uses Tweepy to iteract with twitter, Heroku for deployment, psycopg2 and postgresql for backend database applications, and latent dirichlet allocation for topic classification. The two main features of this bot are status postings and liking tweets that fit certain topics. Connections and cursors to the database are handled using nultithreading and connection pools offered by python's native multithreading library.


##Setting up Twitter and Heroku
There are many existing resources online that do a great job with explaining how to set up and obtain Twitter credentials. Heroku's website also already has very helpful documentation to get started
with that. A Google search can easily reveal a few of these resources but listed below are some that I referenced many times:  
[Apply for Twitter access](https://developer.twitter.com/en/apply-for-access)  
[Helpful link to deploy on Heroku](https://shiffman.net/a2z/bot-heroku/)  
[Using NLTK on Heroku](https://devcenter.heroku.com/articles/python-nltk)  

To replicate this specific bot, download this repo and download all required dependencies in the `requirements.txt` file using the following command:  
```$ pip install -r requirements.txt```  


Also, make sure to fill in your Twitter credentials into Heroku as Config variables. Adding these as variables directly in your code is not ideal. This bot uses python's OS module to retrieve credentials. You can see this in `main.py`:  
```python
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_PORT = os.environ['DB_PORT']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
```
You will also need to supply your twitter bot's screen name in the same manner. So far, the screen name is only referenced in the `find_friends.py` file  

##Status Publishing Feature
Text for posts are prewritten and stored in a database. The database is arranged so that each entry is composed of an integer ID and the tweet text.  

To post a tweet, the bot retrieves an entry from the database and uses tweepy to post. After that entry is posted, it is deleted from the database. Currently, the bot is configured to post every 6 hours.  

Schema for the tweets table:  
Id | Tweet
---|---
1 | text
  

##Tweet Topic Prediction Feature
The tweet topic prediction feature uses latent dirichlet allocation to extract topics from tweets. The model for this feature takes the dirichlet distribution as a feature vector and transfers it to a standard gradient descent classification algorithm. For more details on how I actually trained the model used in this bot, Take a look at [my other repo where I show the actual training script.](https://github.com/hrazo7/LDA-tweet-classification) Code in that repo was adapted from [this repo by Marc Kelechava](https://github.com/marcmuon/nlp_yelp_review_unsupervised). [Marc's Medium article](https://towardsdatascience.com/unsupervised-nlp-topic-models-as-a-supervised-learning-input-cf8ee9e5cf28) also goes into a bit more detail. The original authors of this method where the LDA distribution is used as a feature vector for another classification algorithm are Xuan-Hieu Phan, Le-Minh Nguyen, and Susumu Horiguchi. Their paper can be found [here](http://gibbslda.sourceforge.net/fp224-phan.pdf).  

To obtain tweets, this bot uses a combination of twitter streams and iteration of user timelines. The twitter stream method obtains up to 1200 streams in one iteration. The user timelines method gets the single latest tweet from the friends of the authenticated user for each iteration. Both methods return the posting time, source stream (custom feature), status id, user id, screen name, status text, number of likes, number of retweets, and favorited boolean for each tweet object. All this information is stored in the database with schema:  

createdAt | sourceStream | statusID | userID | screenName | tweetText | numLikes | numRetweets | favorited
---|---|---|---|---|---|---|---|---|---
2019-01-01 23:23 | general stream | 1234 | 5678 | exampleName | exampleText | 332 | 43 | True
2019-01-01 23:23 | friend stream | 1234 | 5678 | exampleName | exampleText | 420 | 66 | True
2019-01-01 23:23 | friend stream | 1234 | 5678 | exampleName | exampleText | 10995 | 3 | True
2019-01-01 23:23 | general stream | 1234 | 5678 | exampleName | exampleText | 190 | 69 | True


After each stream method is complete, the bot iterates through the database table and prepares each status text entry for classification. The preparation includes removing twitter mentions, removing links, making all letters lowercase, removing stopwords, tokenizing, and converting to bigrams. The saved LDA model is then used to predict which topic the status would fall into. Only statuses with scores higher than 0.85 are considered for future action. If a status fulfills the score minimum, the bot will favorite it.  

After the bot is done collecting, cleaning, and classifying statuses, it drops the table where everything was being stored. This is done in order to comply with any data storage limits provided by Heroku. Future versions of this bot do plan on implementing a long-term data storage system. This is also why the streams collect more information besides the status text. Stay tuned!  




##References/Other Helpful Links
[Wikipedia entry on Latent Dirichlet Allocation](https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation)  
[Additional article on Latent Dirichlet Allocation](https://towardsdatascience.com/light-on-math-machine-learning-intuitive-guide-to-latent-dirichlet-allocation-437c81220158)  
[Additional article on Latent Dirichlet Allocation](https://towardsdatascience.com/nlp-extracting-the-main-topics-from-your-dataset-using-lda-in-minutes-21486f5aa925)  
[Marc Kelechava's repo on LDA](https://github.com/marcmuon/nlp_yelp_review_unsupervised). 
[Marc Kelechava's Medium article on LDA](https://towardsdatascience.com/unsupervised-nlp-topic-models-as-a-supervised-learning-input-cf8ee9e5cf28)
[Blei, D. M., Ng, A. Y., Jordan, M. I. (2003). Latent Dirichlet Allocation. Journal of Machine Learning Research, 993-1022](http://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf)  
[Lin, J. (2016). On The Dirichlet Distribution. Queen's University Department of Mathematics and Statistics](https://mast.queensu.ca/~communications/Papers/msc-jiayu-lin.pdf)  
[Examples of Twitter API use cases](https://realpython.com/twitter-bot-python-tweepy/#watching-for-twitter-activity)  
[Intro to Tweet objects](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object)  


