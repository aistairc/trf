import unittest

from trf.acceptability import Acceptability
from trf.util import check_executable


class TestAcceptability(unittest.TestCase):

    def setUp(self):

        check_executable('rnnlm')

        self.text = '英語と呼ばれる\n'
        self.delimiter = '\n'
        self.rnnlm_model_path = 'data/jawiki-20160818-100M-words'
        self.acceptability = \
            Acceptability(self.text,
                          self.delimiter,
                          self.rnnlm_model_path)

    def test_log_prob(self):
        scores = self.acceptability._calc_log_prob_scores()
        self.assertAlmostEqual(scores[0], -11.571, places=2)

    def test_unigram_scores(self):

        scores = self.acceptability._calc_unigram_scores()
        self.assertAlmostEqual(scores[0], -31.457, places=2)

    def test_mean_lp_scores(self):

        score = self.acceptability.mean_lp
        self.assertAlmostEqual(score, -2.892, places=2)

    def test_norm_lp_div(self):

        score = self.acceptability.norm_lp_div
        self.assertAlmostEqual(score, -0.3678, places=2)

    def test_norm_lp_sub(self):

        score = self.acceptability.norm_lp_sub
        self.assertAlmostEqual(score, 19.885, places=2)

    def test_slor(self):

        score = self.acceptability.slor
        self.assertAlmostEqual(score, 4.9713, places=2)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
