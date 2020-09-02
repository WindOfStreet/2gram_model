## sentence.py
  实现按语法规则随机生成句子
## twogram.py
  实现一个二元语法模型，语料来自input文件夹下的影评数据。
  语言模型的功能包括：
  1.计算单词的一元概率分布（1-gram）
  2.计算单词的二元联合概率分布（2-gram）
  3.计算句子的2元联合概率分布，计算句子的困惑度
## best_sentence.py
  基于sentence.py实现多个句子生成，并利用2gram模型计算句子的困惑度，返回最佳句子。
