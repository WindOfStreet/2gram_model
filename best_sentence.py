from sentence import Sentence
from twogram import TwoGrams
import pandas as pd
from time import time

def generate_best(sentence_generator, language_model, num_sentence=20, return_num=1):
    if not isinstance(sentence_generator, Sentence):
        raise TypeError()
    if not isinstance(language_model, TwoGrams):
        raise TypeError()

    stn = sentence_generator
    lm = language_model
    score = []
    dict_stn = {}
    for i in range(num_sentence):
        sent = stn.generate('sentence')
        p, ppl = lm.prob_sentence(sent)
        score.append(ppl)
        dict_stn[ppl] = sent
    score.sort(reverse=True)
    return '\n'.join(dict_stn[item] for item in score[:return_num])


if __name__ == '__main__':

    # 句子生成器
    gram = '''
    sentence = evaluate | describe
    evaluate = article* object adv* adj
    article* = article | null
    adv* = null | adv adv* | adv
    describe = article* object adv* verb object*
    object* = null | object
    '''

    corpus = '''
    article = 这 这个 这部
    object = 电影 影片 片子 片儿 他 她 他们 她们 它 它们 男主 男主角 男主角儿 女主 女主角 女主角儿 男配角 女配角 观众 导演
    adv = 太 十分 相当 相当的 真是 真的是 很 非常 非常非常 特别地 相当地 令人 让人 竟然 居然
    adj = 精彩 吸引人 绝了 值得一看 好看 引人入胜 感人 动容  可怜 愤怒 气人 可恶 垃圾 难看 不真实 不现实 帅 崇拜 美丽 漂亮 可恨 惋惜 牛 厉害 有水平 水平不行 辛苦  水了 差 不咋地 刮目相看 赞 赞了
    verb = 出场 上场 出现 消失 牺牲 杀了 打败了 击败 击败了 爱上了 喜欢上 看上了 相中了 憎恨 不喜欢 仇恨 复仇 
    '''
    # adv = 神秘地
    # adj = 不正经
    snt_grt = Sentence()
    snt_grt.set_corpus(corpus)
    snt_grt.set_grammar(gram)
    sentece_eg = snt_grt.generate('sentence')
    print(sentece_eg)

    # 2元语法模型
    t1 = time()
    data_df = pd.read_csv('input/movie_comments.csv')
    model = TwoGrams()
    model.train(data_df.loc[:20000, 'comment'])
    stn = '导演太让人喜欢了'
    print('(p,ppl){}={}'.format(stn, model.prob_sentence(stn)))
    stn1 = '高晓松是土肥圆？'
    print('(p,ppl){}={}'.format(stn1, model.prob_sentence(stn1)))

    # best sentence
    print(generate_best(snt_grt, model, 100000, 20))

