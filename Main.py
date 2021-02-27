from pymongo import MongoClient
from twitterModel.Twitter import Twitter
from onlineClusterModel.SinglePass import SinglePass

tweet_db = MongoClient('mongodb://root:FzDwXxCl.121.$Root$@121.48.165.123:30011')['tweets_database']['tweets-2020-01-01']
cursor = tweet_db.find()

test = SinglePass()
for tweet in cursor:
    test.addTweet(tweet)
    print tweet


