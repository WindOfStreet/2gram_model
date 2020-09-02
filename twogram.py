import pandas as pd
import jieba
from operator import add
from functools import reduce
from collections import defaultdict
import math


# 2元语法模型
class TwoGrams:
    def __init__(self):
        self.wfreq = defaultdict(int)   # 单词词频
        self.wwfreq = defaultdict(int)  # 两个单词组合词频
        self.token_size = 0     # 单词总数
        self.token2_size = 0    # 二元组合个数
        self.jieba = jieba
        self.jieba.add_word('EOS')
        self.jieba.add_word('BOS')

    def add_dict(self, dict_path):
        # 为结巴分词增加字典
        self.jieba.load_userdict(dict_path)

    @staticmethod
    def _add_eosbos(text):
        text = str(text)
        text = 'BOS' + text
        text = text.replace('。', 'EOSBOS')
        text = text.replace('！', 'EOSBOS')
        # if not text.endswith('S'):
        #     text += 'EOS'
        if text.endswith('BOS'):
            text = text[:-3]
        elif not text.endswith('S'):
            text += 'EOS'
        return text

    def train(self, sr):
        sr = sr.apply(self._add_eosbos)
        for text in sr:
            word_list = list(self.jieba.cut(text))
            # print(word_list)
            size = len(word_list)
            for i in range(size - 1):
                ww = word_list[i] + word_list[i + 1]
                self.wwfreq[ww] += 1
            for word in word_list:
                self.wfreq[word] += 1
        self.token_size = reduce(add, self.wfreq.values())
        self.token2_size = reduce(add, self.wwfreq.values())

    def prob_1(self, word):
        if word in self.wfreq:
            p = self.wfreq[word] / self.token_size
        else:
            p = 0.1 / self.token_size
        return p

    def prob_2(self, w1, w2):
        if w1 + w2 in self.wwfreq:
            p = self.wwfreq[w1 + w2] / self.wfreq[w1] * self.prob_1(w1)
            # p = self.wwfreq[w1 + w2] / self.token2_size * self.prob_1(w1)
        else:
            p = self.prob_1(w1) * self.prob_1(w2)
        # print('{}{}={}'.format(w1,w2,p))
        return p

    #
    def prob_sentence(self, sentence):
        """
        计算句子的2元联合概率和困惑度
        :param sentence: 未分词的整句
        :return: 概率，困惑度。dtype=float,float
        """
        word_list = self.jieba.lcut('BOS' + sentence + 'EOS')
        size = len(word_list)
        prob = 1
        for i in range(size - 1):
            prob *= self.prob_2(word_list[i], word_list[i + 1])
        perplexity = math.pow(prob, -1.0/(size-1))
        return prob, perplexity

    def calc_perplexity(self, tokens):
        """
        计算已分词的句子困惑度
        :param tokens: 句子各词语按顺序排列
        :return: 困惑度，dtype=float
        """
        if not isinstance(tokens, list):
            raise TypeError("parameter must be list.")
        word_list = tokens
        word_list.insert(0, 'BOS')
        word_list.append('BOS')
        size = len(word_list)
        prob = 1
        for i in range(size - 1):
            prob *= self.prob_2(word_list[i], word_list[i + 1])
        perplexity = math.pow(prob, -1.0/(size-1))
        return perplexity



if __name__ == '__main__':
    data_df = pd.read_csv('input/movie_comments.csv')
    model = TwoGrams()
    model.train(data_df.loc[:5000, 'comment'])
    # stn = '想吐恶心看了'
    # stn = '看了恶心想吐'
    stn = '看恶心了吐想'
    # stn = '句子越长概率越低了'
    # stn = '诚意满满，全程无尿点。吴京非常帅，剧情比战狼1好看'
    # stn = '诚意满满，全程无尿点。'
    # stn = '电影这部好看真！'
    # stn = '这部电影真好看！'
    print('{} = （p,perplexity）={}'.format(stn, model.prob_sentence(stn)))

    '''
    看了恶心想吐 = 3.784858337654162e-27
    想吐恶心看了 = 1.5801957539091666e-28
    
    电影这部好看真！ = 4.3787237551975893e-38
    这部电影真好看！ = 1.3273847331879573e-33
    
    诚意满满，全程无尿点。吴京非常帅，剧情比战狼1好看多了 = 1.2865785540358595e-92
    诚意满满，全程无尿点。吴京非常帅，剧情比战狼1好看 = 6.715866109638173e-85
    诚意满满，全程无尿点。 = 1.2075710107390608e-41
    '''

    '''
    （p,perplexity）=
    看了恶心想吐 = (3.784858337654162e-27, 25331.353477078144)
    想吐恶心看了 = (1.5801957539091666e-28, 43007.8948189939)
    看恶心了吐想 = (1.4777576396098927e-31, 137530.6401508262)
    
    电影这部好看真！ = (4.3787237551975893e-38, 1684387.7545455662)
    这部电影真好看！ = (1.3273847331879573e-33, 301648.05563151505)  
    
    诚意满满，全程无尿点。吴京非常帅，剧情比战狼1好看多了 = (1.2865785540358595e-92, 127359.49144475235)
    诚意满满，全程无尿点。吴京非常帅，剧情比战狼1好看 = (6.715866109638173e-85, 182308.1664348822)
    诚意满满，全程无尿点。 = (1.2075710107390608e-41, 700553.0785516506)
    '''