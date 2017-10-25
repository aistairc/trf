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
        self.assertAlmostEqual(analyser.mean_tree_depths, 1.0)

        text = '踊る人を見た。'
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.mean_tree_depths, 2.0)

        text = 'エサを食べるネコを眺めた。'
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.mean_tree_depths, 3.0)

    def test_mean_depth(self):

        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.mean_tree_depths, 2.0)

    def test_mean_n_mrphs(self):
        # 宮澤賢治「銀河鉄道の夜」より
        text = ("カムパネルラが手をあげました。"
                "それから四、五人手をあげました。"
                "ジョバンニも手をあげようとして、いそいでそのままやめました。")
        analyser = Analyser(text, delimiter='。')
        self.assertAlmostEqual(analyser.mean_n_mrphs, 27 / 3)

    def test_n_types(self):
        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')
        self.assertEqual(analyser.n_types, 10)

    def test_n_mrphs(self):
        text = ''.join(['ご飯を食べた。',
                        '踊る人を見た。',
                        'エサを食べるネコを眺めた。'])
        analyser = Analyser(text, delimiter='。')
        self.assertEqual(analyser.n_mrphs, 13)

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
            elif k == "動詞":
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
        modal_counts = analyser.rs_modality

        r_evidences = modal_counts['認識-証拠性']
        r_dicisions = modal_counts['意志']

        self.assertAlmostEqual(r_evidences, 1 / 3)
        self.assertAlmostEqual(r_dicisions, 2 / 3)

    def test_conditional(self):

        sentences = ['ご飯を食べるらしい。',
                     '晴れたならば、そして元気ならば、ご飯を食べるつもりだ。',
                     '元気ならばご飯を食べるつもりだ。']
        n = len(sentences)
        text = ''.join(sentences)

        analyser = Analyser(text, delimiter='。')
        r_conditional = analyser.r_conditional

        self.assertAlmostEqual(r_conditional, 2 / 3)


if __name__ == '__main__':
    unittest.main()
