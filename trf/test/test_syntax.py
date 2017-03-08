#!/usr/bin/env python

import unittest

from trf.tree import Syntax


class TestTree(unittest.TestCase):

    def test_tree_depth_one(self):

        lines = ['ご飯を食べた',
                 '顔を洗った']
        tree = Syntax('\n'.join(lines), delimiter='\n')
        self.assertAlmostEqual(tree.calc_mean_tree_depth(), 1.0)

    def test_tree_depth_two(self):

        lines = ['踊る人を見た']
        tree = Syntax('\n'.join(lines), delimiter='\n')
        self.assertAlmostEqual(tree.calc_mean_tree_depth(), 2.0)

    def test_tree_depth_tree(self):

        lines = ['エサを食べるネコを眺めた']
        tree = Syntax('\n'.join(lines), delimiter='\n')
        self.assertAlmostEqual(tree.calc_mean_tree_depth(), 3.0)

if __name__ == '__main__':
    unittest.main()
