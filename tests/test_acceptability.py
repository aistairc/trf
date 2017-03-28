# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

import unittest
import warnings

class TestAcceptability(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def test_get_logprob(self):
        accep = Acceptability('rnnlm.output', 'uniq.dat', 'test.input')



if __name__ == '__main__':
    unittest.main()
