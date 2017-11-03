import unittest
import warnings
import tempfile

from trf.acceptability import Acceptability
from trf.util import check_executable


class TestAcceptability(unittest.TestCase):

    def setUp(self):

        check_executable('rnnlm')

        self.text = '英語 と 呼ば れる\n'
        self.rnnlm_model_path = 'data/jawiki-20160818'
        self.acceptability = Acceptability(self.text, self.rnnlm_model_path)

    def test_rnnlm_scores(self):
        scores = self.acceptability.rnnlm_scores
        self.assertAlmostEqual(scores[0], -11.295, places=2)

    def test_unigram_scores(self):

        scores = self.acceptability.unigram_scores
        self.assertAlmostEqual(scores[0], -14.098, places=2)

    def test_mean_unigram_scores(self):

        scores = self.acceptability.mean_unigram_scores
        self.assertAlmostEqual(scores[0], -14.098, places=2)

    def test_normalized_scores_div(self):

        scores = self.acceptability.normalized_scores_div
        self.assertAlmostEqual(scores[0], -14.098, places=2)

    def test_normalized_scores_sub(self):

        scores = self.acceptability.normalized_scores_sub
        self.assertAlmostEqual(scores[0], -14.098, places=2)

    def test_normalized_scores_len(self):

        scores = self.acceptability.normalized_scores_len
        self.assertAlmostEqual(scores[0], -14.098, places=2)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
