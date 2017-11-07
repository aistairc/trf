import sys
import argparse
from typing import List

from trf.analyser import Analyser
from trf.acceptability import Acceptability
from trf.util import check_executable


def translate(en: str):

    if en == 'n_sentences':
        return '文数'
    elif en == 'mean_n_mrphs':
        return '平均文長'
    elif en == 'n_tokens':
        return 'トークン数'
    elif en == 'n_types':
        return 'タイプ数'
    elif en == 'mean_tree_depths':
        return '係り受け木の深さ'
    elif en == 'r_conditional':
        return '仮定節'
    elif en == 'mean_loglikelihood':
        return '言語モデルの対数尤度'
    elif en == 'acceptability_div':
        return '容認度 (Norm LP (Div))'
    elif en == 'acceptability_sub':
        return '容認度 (Norm LP (Sub))'
    elif en == 'acceptability_slor (SLOR)':
        return '容認度'
    else:
        return en


class Metric:
    def __init__(self, name: str, val: str):

        self.name = name
        self.val = val
        self.name_ja = translate(name)

    def __str__(self):
        return '\t'.join([self.name_ja, self.val])


class Section:

    def __init__(self, cat: str, metrics: List[Metric]):

        self.cat = cat
        self.metrics = metrics
        if cat == 'basic':
            self.cat_ja = '基本指標'
        elif cat == 'vocabulary':
            self.cat_ja = '語彙に基づく指標'
        elif cat == 'syntax':
            self.cat_ja = '統語情報に基づく指標'
        elif cat == 'language_model':
            self.cat_ja = '言語モデルに基づく指標'
        else:
            self.cat_ja = ''

    def show(self, lang: str='ja'):
        if lang == 'ja':
            print('[{}]'.format(self.cat_ja))
            for metric in self.metrics:
                print('{}={}'.format(metric.name_ja, metric.val))
        else:
            print('Unsupported language')
            sys.exit(1)


def main():

    executables = ['juman', 'knp', 'rnnlm']
    for e in executables:
        check_executable(e)

    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--filename',
                        type=str,
                        help='target text')

    parser.add_argument('--delimiter',
                        type=str,
                        default='\n',
                        help='features to calculate')

    parser.add_argument('-m',
                        '--rnnlm-model-path',
                        type=str,
                        default='data/jawiki-20160818-100M-words',
                        help='RNNLM model path')

    parser.add_argument('--output-lang',
                        type=str,
                        default='ja',
                        help='ja')

    args = parser.parse_args()

    text = ''
    if args.filename is not None:
        with open(args.filename, mode='r') as f:
            text = f.read().replace('\n', '')
    else:
        text = sys.stdin.read()

    analyser = Analyser(text, delimiter=args.delimiter)

    metrics = []
    metrics.append(Metric('n_sentences', analyser.n_sentences))
    metrics.append(Metric('mean_n_mrphs', analyser.mean_n_mrphs))
    metrics.append(Metric('n_tokens', analyser.n_chunks))
    metrics.append(Metric('n_types', analyser.n_types))
    Section('basic', metrics).show()

    metrics = []
    for k, v in analyser.rs_pos.items():
        metrics.append(Metric('品詞：{}'.format(k),
                              '{:.2f}'.format(v)))
    Section('vocabulary', metrics).show()

    metrics = []
    metrics.append(Metric('mean_tree_depths',
                          '{:.2f}'.format(analyser.mean_tree_depths)))
    metrics.append(Metric('r_conditional',
                          '{:.2f}'.format(analyser.r_conditional)))
    for k, v in analyser.rs_modality.items():
        metrics.append(Metric('モダリティ：{}'.format(k),
                              '{:.2f}'.format(v)))
    Section('syntax', metrics).show()

    metrics = []
    acceptability = \
        Acceptability(text,
                      args.delimiter,
                      args.rnnlm_model_path)
    score = acceptability.mean_loglikelihood
    score = 'None' if score is None else '{:.2f}'.format(score)
    metrics.append(Metric('mean_loglikelihood', score))
    normalized_score = acceptability.normalized_scores_len
    metrics.append(Metric('norm_len', normalized_score))
    Section('language_model', metrics).show()


if __name__ == '__main__':
    main()
