# my sentence generator
import random
# from numpy import random


# 给定语法和语料，随机生成句子
class Sentence:

    def __init__(self):
        self.grammar = {}
        self.corpus = {}
        self.word_attr_list = []

    # 将输入的语料字符串转换为dict
    def set_corpus(self, corpus_str, line_split='\n', split='='):
        for line in corpus_str.strip().split(line_split):
            key = line.split(split)[0].strip()
            words = line.split(split)[1].split(' ')
            while '' in words:
                words.remove('')
            for i in range(len(words)):
                words[i] = words[i].strip()
            self.corpus[key] = words

    def get_word(self, word_attr):
        if word_attr in self.corpus:
            random.shuffle(self.corpus[word_attr])
            return random.choice(self.corpus[word_attr])
        else:
            return ""

    def get_words(self, word_attr_list):
        sentence = []
        for attr in word_attr_list:
            sentence.append(self.get_word(attr))
        while '' in sentence:
        return ''.join(sentence)

    # 将输入的字符串格式的语法转换为dict
    def set_grammar(self, grammar_str, line_split='\n', split='='):
        for line in grammar_str.strip().split(line_split):
            key, items = line.split(split)
            self.grammar[key.strip()] = []
            if items.find('|') > 0:
                for x in items.split('|'):
                    self.grammar[key.strip()].append(x.split())
            else:
                key, values = line.split(split)
                self.grammar[key.strip()] = [values.split()]

    # 句子词性序列生成
    def _generate_gram_seq(self, target):
        if target not in self.grammar.keys():
            return self.word_attr_list.extend([target])
        random.shuffle(self.grammar[target])
        next_item = random.choice(self.grammar[target])
        rst = []
        for i in range(len(next_item)):
            self._generate_gram_seq(next_item[i])
        return self.word_attr_list

    # 句子生成
    def generate(self, target):
        self.word_attr_list = []
        rst = self._generate_gram_seq(target)
        return self.get_words(rst)

    # 多句生成
    def generate_n(self, target, n):
        n_words = []
        for i in range(n):
            n_words.append(self.generate(target))
        return ''.join(n_words)


if __name__ == '__main__':

    # 语法中的空格表示前后两个规则串联，| 表示取其前后规则之一
    simple_grammar = """
    sentence = Person verb_phrase
    noun_phrase = Article Adj* noun
    Adj* = null | Adj Adj* | Adj | Adj               
    verb_phrase = verb noun_phrase Loc
    """
    simple_corpus = '''
    Article =  一个 这个
    Person = 你 我 他 他们 我们
    noun =  床 卡车 月球 猪
    verb = 站在 坐在 躺在
    Adj =  美丽的 遥远的 小小的
    Loc = 上面 下面 左边 右边 前面 后面
    '''

    Honor_of_Kings_grammar = '''
    battle_scribe = Heros position_phrase verb_phrase Hero punctuation
    position_phrase = prep position 
    Heros = Hero | Hero and Heros
    verb_phrase = adv verb
    '''
    Honor_of_Kings_Corpus = '''
    Hero = 后裔 孙尚香 盾山 裴擒虎 蔡文姬 凯 东方曜 嬴政 孙悟空
    verb = 击杀了 输给了 遭遇了 
    adv = 吃力地 轻松地 惊险地 令人震惊地
    position = 河道 红区 蓝区 中路 上路 下路
    and = 和 与 带着
    prep = 在
    punctuation = 。 ! 
    '''


    snt_grt = Sentence()
    snt_grt.set_corpus(Honor_of_Kings_Corpus)
    snt_grt.set_grammar(Honor_of_Kings_grammar)
    sentece_eg = snt_grt.generate('battle_scribe')
    print(sentece_eg)

    senteces_eg = snt_grt.generate_n('battle_scribe', 5)
    print(senteces_eg)





