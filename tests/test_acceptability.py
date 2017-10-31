import unittest
import warnings
import tempfile

from trf.acceptability import Acceptability


class TestAcceptability(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_logprob(self):

        rnnlm_output_file = tempfile.NamedTemporaryFile(delete=True)
        rnnlm_output_file.write(b'-14.7579\n')
        rnnlm_output_file.seek(0)

        sentence_file = tempfile.NamedTemporaryFile(delete=True)
        sentence_file.write(b'he always plays baseball\n')
        sentence_file.seek(0)

        word_freq = {'he': 386343,
                     'always': 29482,
                     'plays': 2559,
                     'baseball': 275,
                     'にゃーん': 1}

        word_freq_file = tempfile.NamedTemporaryFile(delete=True)
        s = '\n'.join(['{:>10} {}'.format(v, k) for k, v in word_freq.items()])
        word_freq_file.write(str.encode(s))
        word_freq_file.seek(0)

        a = Acceptability(rnnlm_output_file.name,
                          word_freq_file.name,
                          sentence_file.name)

        self.assertAlmostEqual(a.unigram_lmscores[0], 30.18, places=2)

        rnnlm_output_file.close()
        word_freq_file.close()
        sentence_file.close()



if __name__ == '__main__':
    unittest.main()
