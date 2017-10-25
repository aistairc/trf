#!/usr/bin/env python

import unittest
import warnings

from trf.analyser import Analyser


class TestAnalyser(unittest.TestCase):

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
        analyser = Analyser(text, delimiter='。')
        self.assertEqual(analyser.n_sentences, 3)

    def test_depth(self):

        text = 'ご飯を食べた。'
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.calc_mean_tree_depth(), 1.0)

        text = '踊る人を見た。'
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.calc_mean_tree_depth(), 2.0)

        text = 'エサを食べるネコを眺めた。'
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.calc_mean_tree_depth(), 3.0)

    def test_mean_depth(self):

        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.calc_mean_tree_depth(), 2.0)

    def test_mean_sentence_length(self):
        # 宮澤賢治「銀河鉄道の夜」より
        text = ("カムパネルラが手をあげました。"
                "それから四、五人手をあげました。"
                "ジョバンニも手をあげようとして、いそいでそのままやめました。")
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.calc_mean_sentence_length(), 27 / 3)

    def test_num_of_types(self):
        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')
        self.assertEqual(analyser.calc_num_of_types(), 10)

    def test_num_of_mrphs(self):
        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')
        self.assertEqual(analyser.calc_num_of_mrphs(), 13)

    def test_ratio_of_pos(self):
        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')

        for k, v in analyser.pos_rates.items():
            if k == "名詞":
                noun = v
            elif k == "助詞":
                func = v
            elif k == "動詞" :
                verb = v

        self.assertAlmostEqual(noun, 4.0 / 13)
        self.assertAlmostEqual(func, 4.0 / 13)
        self.assertAlmostEqual(verb, 5.0 / 13)

    def test_modality(self):

        sentences = ['ご飯を食べるらしい。',
                     'ご飯を食べるつもりだ。',
                     'ご飯を食べるつもりだ。']
        n = len(sentences)
        text = ''.join(sentences)

        analyser = Analyser(text, delimiter='。')
        modal_counts = analyser.modality_rates

        r_evidences = modal_counts['認識-証拠性']
        r_dicisions = modal_counts['意志']

        self.assertAlmostEqual(r_evidences, 1 / 3)
        self.assertAlmostEqual(r_dicisions, 2 / 3)


if __name__ == '__main__':
    unittest.main()
