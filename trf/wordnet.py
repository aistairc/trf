#!/usr/bin/env python2.6
# encoding: utf-8

import sys
import sqlite3
from collections import namedtuple
import MeCab
import numpy as np

"""
link
  syns - Synonyms
  hype - Hypernyms
  inst - Instances
  hypo - Hyponym
  hasi - Has Instance
  mero - Meronyms
  mmem - Meronyms --- Member
  msub - Meronyms --- Substance
  mprt - Meronyms --- Part
  holo - Holonyms
  hmem - Holonyms --- Member
  hsub - Holonyms --- Substance
  hprt - Holonyms -- Part
  attr - Attributes
  sim - Similar to
  entag - Entails
  causg - Causes
  dmncg - Domain --- Category
  dmnug - Domain --- Usage
  dmnrg - Domain --- Region
  dmtcg - In Domain --- Category
  dmtug - In Domain --- Usage
  dmtrg - In Domain --- Region
  antsg - Antonyms

lang (default: jpn)
  jpn - Japanese
  eng - English
"""

class WordNet:


    def __init__(self):
        self.conn = sqlite3.connect("./lib/wnjpn-1.1.db")
        self.Word = namedtuple('Word', 'wordid lang lemma pron pos')
        self.Sense = namedtuple('Sense', 'synset wordid lang rank lexid freq src')
        self.Synset = namedtuple('Synset', 'synset pos name src')
        self.SynLink = namedtuple('SynLink', 'synset1 synset2 link src')

    def __getWords(self, lemma):
      cur = self.conn.execute("select * from word where lemma=?", (lemma,))
      return [self.Word(*row) for row in cur]

    def __getWord(self, wordid):
      cur = self.conn.execute("select * from word where wordid=?", (wordid,))
      return self.Word(*cur.fetchone())


    def __getSenses(self, word):
      cur = self.conn.execute("select * from sense where wordid=?", (word.wordid,))
      return [self.Sense(*row) for row in cur]

    def __getSense(self, synset, lang='jpn'):
      cur = self.conn.execute("select * from sense where synset=? and lang=?",
                         (synset,lang))
      row = cur.fetchone()
      return row and self.Sense(*row) or None

    def __getSynset(self, synset):
      cur = self.conn.execute("select * from synset where synset=?", (synset,))
      return self.Synset(*cur.fetchone())

    def __getSynLinks(self, sense, link):
      cur = self.conn.execute("select * from synlink where synset1=? and link=?",
                         (sense.synset, link))
      return [self.SynLink(*row) for row in cur]

    def __getSynLinksRecursive(self, senses, link, depth_list, lang='jpn', _depth=0):

        for sense in senses:
            synLinks = self.__getSynLinks(sense, link)

            if synLinks:
                """
                print ' '.join([' '*2*_depth,
                                getWord(sense.wordid).lemma,
                                getSynset(sense.synset).name,
                                    str(_depth)])
                """
                depth_list.append(_depth)

            _senses = []
            for synLink in synLinks:
                sense = self.__getSense(synLink.synset2, lang)
                if sense:
                    _senses.append(sense)

            self.__getSynLinksRecursive(_senses, link, depth_list, lang, _depth+1)

        if _depth == 0:
            return depth_list if depth_list else [0] # リンクが無い単語はdepth list=[0]として返す

    def load_file(self, fname):
        dataset = []
        with open(fname, "r") as f:
            next(f) # ignore csv head
            for line in f:
                row = line.strip().split("\t")
                dataset.append(row)
        return dataset

    def wakati_text(self, text):
        """ テキストから一般名詞だけを取り出す
        """
        m = MeCab.Tagger("-Ochasen")
        surface_list = []
        node = m.parseToNode(text)
        while node:
            feature = node.feature.split(",")
            pos = feature[0]
            pos_type = feature[1]
            if pos == "名詞" and pos_type == "一般":
                surface_list.append(node.surface)
            node = node.next
        return surface_list

    def get_average_thesaurus_depth(self, surface_list):
        """ シソーラスの深さを取得
            Parameters:
                surface_list : 分析対象のテキスト中の単語リスト(一般名詞のみ)
        """
        max_depth_list = []
        for surface in surface_list:
            #print "- - - - - - - - - - - "
            words = self.__getWords(surface.decode('utf-8'))
            #print "surface:", surface
            if words:
                sense = self.__getSenses(words[0])
                #print "words[0]:", words[0]
                #print "sense:", sense
                #print "len(sys.argv):", len(sys.argv)
                #link = len(sys.argv)>=3 and sys.argv[2] or 'hypo'
                #lang = len(sys.argv)==4 and sys.argv[3] or 'jpn'

                link = 'hype'
                lang = 'jpn'
                depth_list = self.__getSynLinksRecursive(sense, link, [], lang, _depth=0)
                max_depth = max(depth_list)
                #print "max_depth:", max_depth

                if max_depth != 0:
                    max_depth_list.append(max_depth)
                    #print ",".join([surface, str(max_depth)])
            else:
                continue

        if max_depth_list:
            return np.mean(max_depth_list)
        else:
            return "NA"

if __name__ == '__main__':

    wn = WordNet()

    dataset = wn.load_file(sys.argv[1])
    for (code, date, text) in dataset:
        surface_list = wn.wakati_text(text)
        print wn.get_average_thesaurus_depth(surface_list)
        #exit()
