#!/usr/bin/env python

from __future__ import unicode_literals

import unittest
import warnings

from trf.syntax import Syntax


class TestSyntax(unittest.TestCase):

    def setUp(self):
        # ``warnings='ignore'`` is used to suppress ``ResourceWarning``.
        # Another solution is to write the following lines when you call KNP.
        # >> knp.subprocess.process.stdout.close()
        # >> knp.juman.subprocess.process.stdout.close()
        warnings.simplefilter('ignore', ResourceWarning)

    def test_n_sentences(self):
        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        syntax = Syntax(text, delimiter='。')
        self.assertEqual(syntax.n_sentences, 3)

    def test_depth(self):

        text = 'ご飯を食べた。'
        syntax = Syntax(text, delimiter='。')
        self.assertAlmostEqual(syntax.calc_mean_tree_depth(), 1.0)

        text = '踊る人を見た。'
        syntax = Syntax(text, delimiter='。')
        self.assertAlmostEqual(syntax.calc_mean_tree_depth(), 2.0)

        text = 'エサを食べるネコを眺めた。'
        syntax = Syntax(text, delimiter='。')
        self.assertAlmostEqual(syntax.calc_mean_tree_depth(), 3.0)

    def test_mean_depth(self):

        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        syntax = Syntax(text, delimiter='。')
        self.assertAlmostEqual(syntax.calc_mean_tree_depth(), 2.0)


if __name__ == '__main__':
    unittest.main()
