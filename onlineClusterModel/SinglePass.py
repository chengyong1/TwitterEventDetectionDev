#coding=utf-8
from Cluster import Cluster
from twitterModel.Twitter import Twitter

class SinglePass(object):
    def __init__(self, threshold):
        # 当前簇列表，只保留最近的100个簇
        self.clustersList = []
        # 相似度阈值，只有当推文与某个簇相似度大于等于此阈值时才会将该推文加入到该簇中
        self.threshold = threshold

    def addTweet(self, tweet):
        """
        在线聚类主函数，传入一条推文，计算该推文与目前已有簇的相似度，找出与当前推文相似度最高的簇，
        如果其相似度大于等于给定阈值，在该推文加入该簇，并更新该簇信息；否则将该推文单独作为一个簇。
        :param tweet: 传入的推文
        :return:
        """
        # 将该推文进行封装
        tweet = Twitter(tweet)
        num = len(self.clustersList)

        # 记录簇列表中与当前推文最相似的簇索引和对应的相似度取值
        mostSimilar = 0.0
        idx = -1
        # 遍历当前簇列表中所有簇，一一计算该推文与这些簇的相似度
        for i in range(num):
            cluster = self.clustersList[i]
            similar = self._fusionSimilar(tweet, cluster)
            if similar > mostSimilar:
                mostSimilar = similar
                idx = i

        if mostSimilar >= self.threshold:
            # 当相似度大于阈值时，将推文放入索引为idx的簇中，并跟新簇信息
            self._update(tweet, idx)
        else:
            # 否则新建一个簇，该簇目前仅包含当前推文，并放入簇列表
            self.clustersList.append(self._createCluster(tweet))

    def _fusionSimilar(self, tweet, cluster):
        """
        计算推文与簇的融合相似度，分为四个方面
            - 地理位置实体相似度
            - 文本相似度
            - 语义相似度
            - 共现相似度
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        geoSimilar = self._getGeoSimilar(tweet, cluster)
        textSimilar = self._getTextSimilar(tweet, cluster)
        senmanticSimilar = self._getSenmanticSimilar(tweet, cluster)
        coOccurrenceSimilar = self._getCoOccurrenceSimilar(tweet, cluster)
        similar = geoSimilar + textSimilar + senmanticSimilar + coOccurrenceSimilar
        return similar

    def _update(self, tweet, idx):
        """
        将推文放入索引为idx的簇中，更新簇中各信息
        :param tweet: 推文
        :param idx: 簇索引
        :return:
        """
        cluster = self.clustersList[idx]


    def _createCluster(self, tweet):
        pass

    def _getGeoSimilar(self, tweet, cluster):
        """
        计算地理位置相似度，如果推文或者簇中无地理实体，则相似度为0.5；如果推文和簇中地理位置实体相同，则为1；如果不同则为0
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        tweetLocs = tweet.getLocs()
        clusterLocs = cluster.getLocFreq()
        if len(tweetLocs) == 0 or len(clusterLocs) == 0:
            return 0.5
        for tweetLoc in tweetLocs:
            if clusterLocs[tweetLoc] != 0:
                return 1.0
        return 0.0

    def _getTextSimilar(self, tweet, cluster):
        """
        文本相似度，传入推文和簇的单词权重字典，利用余弦相似度计算其相似度
        :param tweet: 推文
        :param cluster: 簇
        :return:
        """
        tweetWords = tweet.getWordsWeight()
        clusterWords = cluster.getWordsWeight()
        common = 0.0
        for word, weight in tweetWords.items():
            common += clusterWords[word] * weight
        if common <= 0.0:
            return 0.0
        # 推文词权重字典的模值
        norm1 = 0.0
        for weight in tweetWords.values():
            norm1 += weight * weight
        norm1 = norm1 ** 0.5
        # 簇词权重字典的模值
        norm2 = 0.0
        for weight in clusterWords.values():
            norm2 += weight * weight
        norm2 = norm2 ** 0.5
        ret = common / (norm1 * norm2)
        return ret

    def _getSenmanticSimilar(self, tweet, cluster):
        return 0

    def _getCoOccurrenceSimilar(self, tweet, cluster):
        return 0
