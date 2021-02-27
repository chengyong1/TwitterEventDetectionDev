#coding=utf-8
from Cluster import Cluster
from twitterModel.Twitter import Twitter

class SinglePass(object):
    def __init__(self):
        # 当前簇列表，只保留最近的100个簇
        self.clustersList = []

    def addTweet(self, tweet):
        tweet = Twitter(tweet)
        