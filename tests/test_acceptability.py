# -*- coding:utf-8 -*-
from __future__ import division, unicode_literals, print_function
import sys
import math
import argparse
import re
from lib import config
import numpy as np

""" 実行方法
$ cat [各文に対するrnnlmのスコア(rnnlm.output)] | python acceptability.py [学習データの語彙ファイル(uniq.dat)] [acceptabilityを計算したい文(test.input)] [code, date, idファイル]
"""

pattern_uniq = re.compile('( )*?(?P<cnt>[0-9]+) (?P<word>.+?)$')


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("uniq",
                        type=str,
                        help="トレーニングデータから作ったuniqデータを指定")
    parser.add_argument("test",
                        type=str,
                        help="acceptabilityを計算したいファイルを指定")
    parser.add_argument("key",
                        type=str,
                        help="証券コード, 提出日, セクションIDの一覧ファイル")
    parser.add_argument("--out",
                        type=str,
                        help="出力先")

    return parser.parse_args()

""" measures
"""
class Acceptability:

    def __init__(self, std_input):

        lmscore = []
        for line in std_input:
            line = line.strip()
            if line == "OOV":
                lmscore.append(None)
            else:
                lmscore.append(float(line))

    def logprob(self, lmscore):
        logprob_list = []
        for score in lmscore:
            logprob_list.append(score)

        return logprob_list


    def meanlp(self, lmscore, sen_len):
        meanlp_list = []
        for rnn, sen in zip(lmscore, sen_len):
            if rnn is not None:
                score = float(rnn)/sen
            else:
                score = None
            meanlp_list.append(score)

        return meanlp_list

    def normlp_div(self, lmscore, unilist):
        normlp_div_list = []
        for rnn, uni in zip(lmscore, unilist):
            if rnn is not None:
                score = - float(rnn)/uni
            else:
                score = None
            normlp_div_list.append(score)

        return normlp_div_list

    def norlp_sub(self, lmscore, unilist):
        normlp_sub_list = []
        for rnn, uni in zip(lmscore, unilist):
            if rnn is not None:
                score =  (float(rnn) - float(uni))
            else:
                score = None
            normlp_sub_list.append(score)

        return normlp_sub_list

    def slor(self, lmscore, unilist, sen_len):
        slor_list = []
        for rnn, uni, sen in zip(lmscore, unilist, sen_len):
            if rnn is not None:
                score = (float(rnn) - uni)/sen
            else:
                score = None
            slor_list.append(score)

        return slor_list

""" io
"""
def read_key_file(filename):
    with open(filename, "r") as input:
        key_list = [line.rstrip() for line in input]
    return key_list

def read_rnnlm_score(lines):
    """ extract only language model scores from std_input
    """
    lmscore = []
    for line in lines:
        line = line.strip()
        if line == "OOV":
            lmscore.append(None)
        else:
            lmscore.append(float(line))
    return lmscore


def read_word(uniqdata):
    d_words = {}
    totalwordcnt = 0

    with open(uniqdata, "r") as input:
        for line in input:
            line = line.strip()
            tmp_cnt, word = line.split()
            cnt = int(tmp_cnt)

            if cnt > 1:
                d_words[word] = cnt
            else:
                d_words["<unk>"] = d_words.get("<unk>", 0) + 1

            totalwordcnt += cnt

    return d_words, totalwordcnt

def read_test_sentence(filename):

    with open(filename, "r") as input:
        list_sentence = [line.rstrip() for line in input]

    return list_sentence

def print_results(sentences, lp, mlp, nlpdiv, nlpsub, slr, lmscore, unilmscore):

    results = zip(sentences, lp, mlp, nlpdiv, nlpsub, slr, lmscore, unilmscore)
    for sen, elp, emlp, enlpdiv, enlpsub, eslr, elmscore, eunilmscore in results :
        print "Input: {} totalwords: {} ".format(sen, len(sen.split()))
        print "RNNLMProb: {} UnigramProb: {} ".format(elmscore, eunilmscore)
        print "logprob: {} MeanLP: {} NormLP(Div): {} NormLP(Sub): {} SLOR: {} ".format(elp, emlp, enlpdiv, enlpsub, eslr)
        print " - - - - -"


""" preprocessing
"""
def calc_unilmscore(sentences, dict_words, total_word_cnt):
    """ calcualte unigram probability of input sentence
    """

    uni_list = []
    for sen in sentences:
        words = sen.split()
        uniscore = 0
        for word in words:
            uniscore += math.log(float(dict_words.get(word, dict_words["<unk>"])) / float(total_word_cnt))
        uni_list.append(uniscore)
    return uni_list

def get_sentence_length(sentences):
    """ calcualte length of input sentences (number of words for each sentence)
    """
    return [len(sen.strip().split()) for sen in sentences]


def print_results_with_csv(sentences,
                           key_list,
                           lp,
                           mlp,
                           nlpdiv,
                           nlpsub,
                           slr,
                           lmscore,
                           unilmscore):
    """ 計算した値を出力
    """
    results = zip(sentences, key_list, lp, mlp, nlpdiv, nlpsub, slr, lmscore, unilmscore)
    column_list = ["SecuritiesCode","FilingDate","SectionID"] + ["logprob", "MeanLP", "NormLP(Div)", "NormLP(Sub)", "SLOR"]
    print ",".join(column_list)
    p_key = key_list[0]
    accep_list = []
    for sen, key, elp, emlp, enlpdiv, enlpsub, eslr, elmscore, eunilmscore in results:
        #print ",".join(map(str,[elp, emlp, enlpdiv, enlpsub, eslr]))

        if None in [elp, emlp, enlpdiv, enlpsub, eslr]: # None行は無視
            continue

        if key == p_key:
            accep_list.append([elp, emlp, enlpdiv, enlpsub, eslr])
        else:

            #転置して指標毎のサブリストに変換
            print ",".join([p_key] + map(str, [np.mean(elem) for elem in np.array(accep_list).T]))

            accep_list = []
            accep_list.append([elp, emlp, enlpdiv, enlpsub, eslr])

        p_key = key

    # 最後の要素
    print ",".join([p_key] + map(str, [np.mean(elem) for elem in np.array(accep_list).T]))

""" main
"""
def main():

    args = parse_argument()

    #辞書読み込み
    dict_words, total_word_cnt = read_word(args.uniq)

    #文章読み込む
    sentences = read_test_sentence(args.test)

    # keyfileを読み込む
    key_list = read_key_file(args.key)

    # extract rnn language model scores
    lmscore = get_lmscore(sys.stdin)

    sen_len = get_sentence_length(sentences)
    unilmscore = calc_unilmscore(sentences, dict_words, total_word_cnt)

    # calculate acceptability of sentences
    lp = logprob(lmscore)
    mlp = meanlp(lmscore, sen_len)
    nlpdiv = normlp_div(lmscore, unilmscore)
    nlpsub = norlp_sub(lmscore, unilmscore)
    slr = slor(lmscore, unilmscore, sen_len)

    # output results
    print_results_with_csv(sentences,
                           key_list,
                           lp,
                           mlp,
                           nlpdiv,
                           nlpsub,
                           slr,
                           lmscore,
                           unilmscore)


if __name__ == "__main__":
    main()
