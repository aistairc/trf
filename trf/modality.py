# -*- encoding: utf-8 -*-

from __future__ import division, unicode_literals

import re
from pyknp import KNP
from collections import Counter

import trf.util as util
from trf.chunk import Chunk


class Modality(object):
    """Class for analyze modality
    """

    def __init__(self, text, delimiter='\n'):
        """
        Args:
            text (str)
            delimiter (str)
        """
        self.sentences = util.split_text(text, delimiter)
        self.n_sentence = len(self.sentences)
        self.rates = self._rates()

    def _rates(self):
        """
        Returns:
            dict(str, float)
        """
        knp = KNP(option="-dpnd-fast -tab")

        modality_counter = Counter()
        chunks = []
        for i, s in enumerate(self.sentences):
            for bnst in knp.parse(s).bnst_list():
                chunk = Chunk(chunk_id=bnst.bnst_id,
                              link=bnst.parent,
                              description=bnst.fstring)
                chunks.append(chunk)

            s = "".join([chunk.description for chunk in chunks])
            ms = set(re.findall("<モダリティ.*?>", s))
            modality_counter += Counter(ms)

            n = len(self.sentences)

        knp.subprocess.process.stdout.close()
        knp.juman.subprocess.process.stdout.close()

        return dict([(k, float(c) / n)
                    for k, c in modality_counter.items()])
