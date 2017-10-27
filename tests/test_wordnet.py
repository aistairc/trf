#!/usr/bin/env python

import unittest

from trf.wordnet import WordNet


class TestAnalyser(unittest.TestCase):

    def setUp(self):
        self.wordnet = WordNet('data/wnjpn.db', 'jpn')

    def test_mean_thesaurus_depth(self):

        surfaces = []
        x = self.wordnet.calc_mean_thesaurus_depths(surfaces)
        self.assertAlmostEqual(x, 0.0)

        # TODO: Check if 8.0 is accurate
        surfaces = ['本']
        x = self.wordnet.calc_mean_thesaurus_depths(surfaces)
        self.assertAlmostEqual(x, 8.0)

        # TODO: Check if 8.5 is accurate
        surfaces = ['本', '大根']
        x = self.wordnet.calc_mean_thesaurus_depths(surfaces)
        self.assertAlmostEqual(x, 8.5)


if __name__ == '__main__':
    unittest.main()
