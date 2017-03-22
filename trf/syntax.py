import numpy as np

from trf.chunk import Chunk
from trf.constant import DefaultOptions
import trf.util as util


class Tree(object):

    def __init__(self, sentence, chunks):
        self.sentence = sentence
        self.chunks = chunks
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

    def depth(self):
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


class Syntax(object):
    """Class for syntactic Analysis
    """

    def __init__(self, text, delimiter='\n'):
        self.text = text
        self.delimiter = delimiter
        self.sentences = util.split_text(self.text, delimiter)
        self.n_sentences = len(self.sentences)
        try:
            from pyknp import KNP
            self.parser = KNP(option=DefaultOptions.KNP)
            self.trees = self._trees()
        except ImportError:
            self.parser = None
            self.trees = None

    def _trees(self):
        """Analyse dependency structure using KNP
        Returns:
            list(trf.Tree)
        """

        results = []

        for sentence in self.sentences:
            chunks = []
            for bnst in self.parser.parse(sentence).bnst_list():
                chunk = Chunk(chunk_id=bnst.bnst_id,
                              link=bnst.parent_id,
                              description=bnst.fstring)
                chunks.append(chunk)

            results.append(Tree(sentence, chunks))

        return results

    def calc_mean_tree_depth(self):
        """Calculate the mean depth of dependency tree
        Returns:
            float: The mean depth of trees
        """
        return np.mean([tree.depth for tree in self.trees])
