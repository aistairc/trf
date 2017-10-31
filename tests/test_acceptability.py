import unittest
import warnings
import tempfile

from trf.acceptability import Acceptability


class TestAcceptability(unittest.TestCase):

    def setUp(self):

        self.text = 'he always plays baseball\n'

        self.rnnlm_output_file = tempfile.NamedTemporaryFile(delete=True)
        self.rnnlm_output_file.write(b'-14.7579\n')
        self.rnnlm_output_file.seek(0)

        word_freq = {'he': 386343,
                     'always': 29482,
                     'plays': 2559,
                     'baseball': 275,
                     'にゃーん': 1}

        self.word_freq_file = tempfile.NamedTemporaryFile(delete=True)
        s = '\n'.join(['{:>10} {}'.format(v, k) for k, v in word_freq.items()])
        self.word_freq_file.write(str.encode(s))
        self.word_freq_file.seek(0)

    def test_unigram_lm_scores(self):

        a = Acceptability(self.text,
                          self.rnnlm_output_file.name,
                          self.word_freq_file.name)
        self.assertAlmostEqual(a.unigram_lm_scores[0], 30.18, places=2)

    def test_mean_unigram_lm_scores(self):

        a = Acceptability(self.text,
                          self.rnnlm_output_file.name,
                          self.word_freq_file.name)
        self.assertAlmostEqual(a.unigram_lm_scores[0], 30.18, places=2)

    def test_lm_scores_normalized_by_div(self):

        a = Acceptability(self.text,
                          self.rnnlm_output_file.name,
                          self.word_freq_file.name)
        self.assertAlmostEqual(a.lm_scores_normalized_by_div[0],
                               0.4889, places=2)

    def test_lm_scores_normalized_by_sub(self):

        a = Acceptability(self.text,
                          self.rnnlm_output_file.name,
                          self.word_freq_file.name)
        self.assertAlmostEqual(a.lm_scores_normalized_by_sub[0],
                               -44.94, places=2)

    def test_lm_scores_normalized_by_len(self):

        a = Acceptability(self.text,
                          self.rnnlm_output_file.name,
                          self.word_freq_file.name)
        self.assertAlmostEqual(a.lm_scores_normalized_by_len[0],
                               -1.875, places=2)

    def tearDown(self):

        self.rnnlm_output_file.close()
        self.word_freq_file.close()


if __name__ == '__main__':
    unittest.main()
