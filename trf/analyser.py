import re
from typing import Dict, List
from collections import Counter

import numpy
from pyknp import KNP, Juman
from janome.tokenizer import Tokenizer  # conditional の検出で使う

from trf.chunk import Chunk
from trf.constant import DefaultOptions
import trf.wordnet as wordnet
import trf.util as util


class Tree:

    def __init__(self,
                 sentence: str,
                 chunks: List[Chunk],
                 surfaces: List[str]):

        self.sentence = sentence
        self.chunks = chunks
        self.surfaces = surfaces
        self.depth = self.depth()

    def find_next_chunk(self, chunk_id, depth):
        """Recursively find the next chunk until reaching the root
        """
        if self.chunks[chunk_id].link == -1:
            return depth
        else:
            next_chunk_id = self.chunks[chunk_id].link
            return self.find_next_chunk(next_chunk_id,
                                        depth + 1)

    def depth(self) -> int:
        """Calculate the mean depth of dependency tree
        Returns:
            int: The depth of given tree
        """
        current_tree_depth = 0

        for i, chunk in enumerate(self.chunks):
            depth = self.find_next_chunk(i, 0)
            if depth > current_tree_depth:
                current_tree_depth = depth

        return current_tree_depth


class Analyser:
    """Class for syntactic Analysis
    """

    def __init__(self, text: str, delimiter: str='\n'):
        self.text = text
        self.delimiter = delimiter
        self.sentences = util.split_text(self.text, delimiter)
        self.n_sentences = len(self.sentences)
        self.knp = KNP(option=DefaultOptions.KNP)
        self.trees = self._trees()
        self.juman = Juman()
        self.rs_pos = self.calc_rs_pos()
        self.n_mrphs = self.calc_n_mrphs()
        self.n_chunks = self.calc_n_chunks()
        self.n_types = self.calc_n_types()
        self.mean_n_mrphs = None \
            if self.n_sentences == 0 \
            else self.n_mrphs / self.n_sentences
        self.rs_modality = self.calc_rs_modality()
        self.r_conditional = None \
            if self.n_sentences == 0 \
            else self.calc_n_conditionals() / self.n_sentences
        self.mean_tree_depths = self.calc_mean_tree_depths()

    def _trees(self) -> Tree:
        """Analyse dependency structure using KNP
        Returns:
            list(trf.Tree)
        """

        results = []

        for sentence in self.sentences:
            chunks = []
            parse_result = self.knp.parse(sentence)
            for bnst in parse_result.bnst_list():
                chunk = Chunk(chunk_id=bnst.bnst_id,
                              link=bnst.parent_id,
                              description=bnst.fstring)
                chunks.append(chunk)
            surfaces = [m.midasi for m in parse_result.mrph_list()]
            results.append(Tree(sentence, chunks, surfaces))

        return results

    def calc_rs_pos(self) -> Dict[str, float]:
        """Calculate the ratio of each pos of words in input text
        Returns:
            float: the ratio of each pos of words in input text
        """
        pos = []
        # TODO: It may take a long time when the number of sentences are large
        for sentence in self.sentences:
            juman_result = self.juman.analysis(sentence)
            pos += [mrph.hinsi for mrph in juman_result.mrph_list()]
        pos_counter = Counter(pos)
        total = sum(pos_counter.values())
        return {name: float(num) / total for name, num in pos_counter.items()}

    def calc_mean_tree_depths(self) -> float:
        """Calculate the mean depth of dependency tree
        Returns:
            float: The mean depth of trees
        """
        return numpy.mean([tree.depth for tree in self.trees])

    def calc_mean_sentence_length(self) -> float:
        """Calculate the mean length (# of morphs) of sentences
        Returns:
            float: the mean length of sentences
        """
        result = 0
        for sentence in self.sentences:
            juman_result = self.juman.analysis(sentence)
            result += len(juman_result.mrph_list())
        return result / self.n_sentences

    def calc_n_sentences(self) -> int:
        """Calculate the number of sentences of input text
        Returns:
            int: the number of sentences of input text splitted by delimiter (default '。')
        """
        return self.n_sentences

    def calc_n_types(self) -> int:
        """Calculate the number of types of input text
        Returns:
            int: the number of types of input text
        """
        surfaces = []
        for sentence in self.sentences:
            juman_result = self.juman.analysis(sentence)
            surfaces += [mrph.midasi for mrph in juman_result.mrph_list()]
        word_type_counter = Counter(surfaces)
        return len(word_type_counter)

    def calc_n_mrphs(self) -> int:
        """Calculate the number of morphemes of input text
        Returns:
            int: the number of morphemes of input text
        """
        n_mrphs = 0
        for sentence in self.sentences:
            juman_result = self.juman.analysis(sentence)
            n_mrphs += len(juman_result.mrph_list())
        return n_mrphs

    def calc_n_chunks(self) -> int:
        # TODO: 共通化
        return sum([len(self.knp.parse(s).bnst_list())
                    for s in self.sentences])

    def calc_rs_modality(self) -> Dict[str, float]:

        modality_counter = Counter()
        for i, s in enumerate(self.sentences):
            chunks = []
            for bnst in self.knp.parse(s).bnst_list():
                chunk = Chunk(chunk_id=bnst.bnst_id,
                              link=bnst.parent,
                              description=bnst.fstring)
                chunks.append(chunk)

            s = "".join([chunk.description for chunk in chunks])
            ms = set(re.findall("<モダリティ-(.+?)>", s))
            modality_counter += Counter(ms)

            n = len(self.sentences)

        return dict([(k, float(c) / n)
                     for k, c in modality_counter.items()])

    def calc_n_conditionals(self) -> int:
        """
        Returns:
            int: the number of sentences that contains one or more conditional clauses
        """
        result = 0

        tokenizer = Tokenizer()
        for s in self.sentences:
            for token in tokenizer.tokenize(s):
                if token.infl_form == '仮定形':
                    result += 1
                    break

        return result

    def calc_mean_thesaurus_depths(self) -> float:
        # TODO: Share the parsing result
        surfaces = []
        tokenizer = Tokenizer()
        for s in self.sentences:
            for token in tokenizer.tokenize(s):
                pos, pos1, _, _ = token.part_of_speech.split(',')
                if pos == '名詞' and pos1 == '一般':
                    surfaces.append(token.surface)

        return wordnet.calc_mean_thesaurus_depths(surfaces)
