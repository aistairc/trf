#!/usr/bin/env python

import unittest

from trf.syntax import Syntax


class TestSyntax(unittest.TestCase):

    def test_depth_one(self):

        lines = ['ご飯を食べた']
        syntax = Syntax('\n'.join(lines), delimiter='\n')
        self.assertAlmostEqual(int(syntax.calc_mean_tree_depth()), 1)

    def test_depth_two(self):

        lines = ['踊る人を見た']
        syntax = Syntax('\n'.join(lines), delimiter='\n')
        self.assertEqual(int(syntax.calc_mean_tree_depth()), 2)

    def test_depth_three(self):

        lines = ['エサを食べるネコを眺めた']
        syntax = Syntax('\n'.join(lines), delimiter='\n')
        self.assertEqual(int(syntax.calc_mean_tree_depth()), 3)

    def test_mean_depth(self):

        lines = ['ご飯を食べた',
                 '踊る人を見た',
                 'エサを食べるネコを眺めた']
        syntax = Syntax('\n'.join(lines), delimiter='\n')
        self.assertAlmostEqual(syntax.calc_mean_tree_depth(), 2.0)


if __name__ == '__main__':
    unittest.main()
