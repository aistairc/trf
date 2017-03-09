# -*- encoding: utf-8 -*-

from __future__ import division, unicode_literals

import re
from pyknp import KNP
from collections import Counter

import trf.util as util
from trf.chunk import Chunk


class Modality(object):

    def __init__(self, text, delimiter='\n'):
        self.sentences = util.split_text(text, delimiter)
        self.n_sentence = len(self.sentences)
        # TODO: io.BufferedReader
        self.rates = self._rates()

    def _rates(self):
        """
        Returns:
            dict(str, float)
        """
        parser = KNP(option="-dpnd-fast -tab")

        modality_counter = Counter()
        chunks = []
        for i, s in enumerate(self.sentences):
            for bnst in parser.parse(s).bnst_list():
                chunk = Chunk(chunk_id=bnst.bnst_id,
                              link=bnst.parent,
                              description=bnst.fstring)
                chunks.append(chunk)

            s = "".join([chunk.description for chunk in chunks])
            ms = set(re.findall("<モダリティ.*?>", s))
            modality_counter += Counter(ms)

            n = len(self.sentences)

        parser.subprocess.process.stdout.close()

        return dict([(k, float(c) / n)
                    for k, c in modality_counter.items()])
