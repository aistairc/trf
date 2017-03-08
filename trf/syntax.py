import numpy as np
import CaboCha


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


class Chunk(object):

    def __init__(self, chunk):
        self.link = chunk.link


class Syntax(object):
    """Class for syntactic Analysis
    """

    def __init__(self, text, delimiter='\n'):
        self.text = text
        self.delimiter = delimiter
        self.trees = self._dependency_structure(text,
                                                delimiter=self.delimiter)

    def _dependency_structure(self, text, delimiter):
        """Analyse dependency structure using CaboCha
        Args:
            text: input text which contains sentences split by delimiter
        Returns:
            list(trf.Tree)
        """

        sentences = self.text.split(delimiter)
        cabocha = CaboCha.Parser()

        results = []

        for sentence in sentences:
            tree = cabocha.parse(sentence)

            chunks = []
            for j in range(tree.chunk_size()):
                chunk = Chunk(tree.chunk(j))
                chunks.append(chunk)

            results.append(Tree(sentence, chunks))

        return results

    def calc_mean_tree_depth(self):
        """Calculate the mean depth of dependency tree
        Returns:
            float: The mean depth of trees
        """
        return np.mean([tree.depth for tree in self.trees])
