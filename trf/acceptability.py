import errno
import os
from typing import Dict, List, Tuple, Union
import tempfile
from subprocess import Popen, PIPE
import math
import numpy
from janome.tokenizer import Tokenizer

import trf.constant as const
from trf.util import split_text


class Acceptability:

    def __init__(self, text: str, delimiter: str, rnnlm_model_path: str):

        self.text = text
        self.sentences = split_text(text, delimiter)  # type: List[str]
        lengths, self.tss = tokenize(self.sentences)

        if not os.path.isfile(rnnlm_model_path):
            raise FileNotFoundError(errno.ENOENT,
                                    os.strerror(errno.ENOENT),
                                    rnnlm_model_path)
        self.rnnlm_model_path = rnnlm_model_path

        self.word_freq, self.n_total_words = self._load_word_freq(threshold=1)

        log_prob_scores = \
            self._calc_log_prob_scores()
        unigram_scores = \
            self._calc_unigram_scores()

        mean_lp_scores = \
            calc_mean_lp_scores(log_prob_scores, lengths)
        norm_lp_div_scores = \
            calc_norm_lp_div_scores(log_prob_scores, unigram_scores)
        norm_lp_sub_scores = \
            calc_norm_lp_sub_scores(log_prob_scores, unigram_scores)
        slor_scores = \
            calc_slor_scores(norm_lp_sub_scores, lengths)

        self.log_prob = average(log_prob_scores)
        self.mean_lp = average(mean_lp_scores)
        self.norm_lp_div = average(norm_lp_div_scores)
        self.norm_lp_sub = average(norm_lp_sub_scores)
        self.slor = average(slor_scores)

    def _calc_log_prob_scores(self) -> List[Union[None, float]]:
        """Get log likelihood scores by calling RNNLM
        """

        textfile = tempfile.NamedTemporaryFile(delete=True)
        content = '\n'.join([''.join(ts) for ts in self.tss]) + '\n'
        textfile.write(str.encode(content))
        textfile.seek(0)

        command = ['rnnlm',
                   '-rnnlm',
                   self.rnnlm_model_path,
                   '-test',
                   textfile.name]
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        output, err = process.communicate()
        lines = [line.strip() for line in output.decode('UTF-8').split('\n')
                 if line.strip() != '']
        scores = []
        for line in lines:
            if line == const.OUT_OF_VOCABULARY:
                scores.append(None)
            else:
                try:
                    score = float(line)
                    scores.append(score)
                except ValueError:
                    pass
        textfile.close()
        return scores

    def _load_word_freq(self, threshold: int) -> Tuple[Dict[str, int], int]:
        n_total_words = 0
        word_freq = {}
        with open(self.rnnlm_model_path, mode='r') as f:
            for line in f:

                n_total_words += 1

                word, freq = line.split(' ')
                freq = int(freq)
                if freq > threshold:
                    word_freq[word] = freq
                else:
                    word_freq['<unk/>'] = word_freq.get('<unk/>', 0) + 1

        return (word_freq, n_total_words)

    def _calc_unigram_scores(self) -> List[float]:

        unigram_scores = []
        for ts in self.tss:
            unigram_score = 0.0

            for t in ts:
                n = float(self.n_total_words)
                x = float(self.word_freq.get(t, self.word_freq['<unk/>']))
                unigram_score += math.log(x / n)

            unigram_scores.append(unigram_score)

        return unigram_scores


def average(xs: List[Union[None, float]]) -> float:
    """Calculate the arithmetic mean of the given values (possibly None)
    >>> '{:.2f}'.format(average([None, 1.0, 2.0]))
    '1.50'
    """
    return numpy.mean([x for x in xs if x is not None])


def calc_mean_lp_scores(log_prob_scores: List[float],
                        lengths: List[int]) -> List[Union[None, float]]:
    r"""
    .. math:
        \frac{%
            \log P_\text{model}\left(\xi\right)
            }{%
              \text{length}\left(\xi\right)
            }
    >>> '{:.3f}'.format(calc_mean_lp_scores([-14.7579], [4])[0])
    '-3.689'
    """
    mean_lp_scores = []
    for score, length in zip(log_prob_scores, lengths):
        x = None \
            if score is None or length == 0 \
            else float(score) / float(length)
        mean_lp_scores.append(x)
    return mean_lp_scores


def calc_norm_lp_div_scores(
        log_prob_scores: List[float],
        unigram_scores: List[float]) -> List[Union[None, float]]:
    r"""
    .. math:
        \frac{%
            \log P_\text{model}\left(\xi\right)
        }{%
            \log P_\text{unigram}\left(\xi\right)
        }
    >>> '{:.3f}'.format(calc_norm_lp_div_scores([-14.7579], [-35.6325])[0])
    '-0.414'
    """
    results = []
    for log_prob, unigram_score in zip(log_prob_scores, unigram_scores):
        if log_prob is None or numpy.isclose(unigram_score, 0.0, rtol=1e-05):
            x = None
        else:
            x = (-1.0) * float(log_prob) / float(unigram_score)
        results.append(x)
    return results


def calc_norm_lp_sub_scores(
        log_prob_scores: List[float],
        unigram_scores: List[float]) -> List[Union[None, float]]:
    r"""
    .. math:
        \log P_\text{model}\left(\xi\right)
            - \log P_\text{unigram}\left(\xi\right)
    >>> '{:.3f}'.format(calc_norm_lp_sub_scores([-14.7579], [-35.6325])[0])
    '20.875'
    """

    results = []
    for log_prob, unigram_score in zip(log_prob_scores, unigram_scores):
        if log_prob is None or numpy.isclose(unigram_score, 0.0, rtol=1e-05):
            x = None
        else:
            x = float(log_prob) - float(unigram_score)
        results.append(x)
    return results


def calc_slor_scores(norm_lp_sub_scores: List[float],
                     lengths: List[int]) -> List[Union[None, float]]:
    r"""Calculate SLOR (Syntactic Log-Odds Ratio)
    .. math:
        \frac{%
            \log P_\text{model}\left(\xi\right)
                - \log P_\text{unigram}\left(\xi\right)
        }{%
            \text{length}\left(\xi\right)
        }
    >>> '{:.3f}'.format(calc_slor_scores([20.8746], [4])[0])
    '5.219'
    """

    results = []
    for norm_lp_sub_score, length in zip(norm_lp_sub_scores, lengths):
        if (norm_lp_sub_score is None) or length == 0:
            x = None
        else:
            x = norm_lp_sub_score / length
        results.append(x)
    return results


def tokenize(sentences: List[str]) -> Tuple[List[int], List[List[str]]]:

    tokenizer = Tokenizer()
    lengths = []
    texts = []
    for s in sentences:
        result = tokenizer.tokenize(s)

        surfaces = [t.surface for t in result]
        lengths.append(len(surfaces))

        text = ' '.join(surfaces)
        texts.append(text)
    return lengths, texts


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
