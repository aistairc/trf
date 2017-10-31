from typing import Dict, List, Tuple, Union
import math
import numpy


class Acceptability:

    def __init__(self,
                 text: str,
                 rnnlm_output_filename: str,
                 wordfreq_filename: str):

        self.lm_scores = self._load_lm_scores(rnnlm_output_filename)

        self.word_freq, self.n_total_words = \
            self._load_word_freq(wordfreq_filename, threshold=1)

        self.sentences = [s.strip() for s in text.split('\n')
                          if s.strip() != '']

        self.unigram_lm_scores = self.calc_unigram_lm_scores()

        self.mean_unigram_lm_scores = self.calc_mean_unigram_lm_scores()

        self.lm_scores_normalized_by_div = \
            self.calc_lm_scores_normalized_by_div()

        self.lm_scores_normalized_by_sub = \
            self.calc_lm_scores_normalized_by_sub()

        self.lm_scores_normalized_by_len = \
            self.calc_lm_scores_normalized_by_len()

    @staticmethod
    def _load_lm_scores(rnnlm_output_filename: str) -> List[Union[None, float]]:
        scores = []
        with open(rnnlm_output_filename, mode='r') as f:
            for line in f:
                line = line.strip()
                if line == "OOV":
                    scores.append(None)
                else:
                    scores.append(float(line))
        return scores

    @staticmethod
    def _load_word_freq(filename: str,
                        threshold: int) -> Tuple[Dict[str, int], int]:
        n_total_words = 0
        word_freq = {}
        with open(filename, mode='r') as f:
            for line in f:

                n_total_words += 1

                freq, word = line.strip().split()
                freq = int(freq)
                if freq > threshold:
                    word_freq[word] = freq
                else:
                    word_freq['<unk/>'] = word_freq.get('<unk/>', 0) + 1

        return (word_freq, n_total_words)

    def calc_unigram_lm_scores(self) -> List[float]:

        unigram_scores = []
        for s in self.sentences:
            unigram_score = 0.0

            for word in s.split():
                n = float(self.n_total_words)
                x = float(self.word_freq.get(word, self.word_freq['<unk/>']))
                unigram_score += math.log(x / n)

            unigram_scores.append(unigram_score)

        return unigram_scores

    def calc_mean_unigram_lm_scores(self) -> List[Union[None, float]]:
        mean_unigram_lm_scores = []
        for score, sentence in zip(self.unigram_lm_scores, self.sentences):
            n = len(self.sentences)
            x = None \
                if score is None or n == 0 \
                else float(score) / float(len(self.sentences))
            mean_unigram_lm_scores.append(x)
        return mean_unigram_lm_scores

    def calc_lm_scores_normalized_by_div(self) -> List[Union[None, float]]:

        normalized_lm_scores = []
        for lm_score, unigram_lm_score in zip(self.lm_scores,
                                              self.unigram_lm_scores):
            x = None \
                if lm_score is None or numpy.isclose(unigram_lm_score, 0.0, rtol=1e-05) \
                else (-1) * float(lm_score) / float(unigram_lm_score)
            normalized_lm_scores.append(x)
        return normalized_lm_scores

    def calc_lm_scores_normalized_by_sub(self) -> List[Union[None, float]]:

        normalized_lm_scores = []
        for lm_score, unigram_lm_score in zip(self.lm_scores,
                                              self.unigram_lm_scores):
            x = None \
                if lm_score is None or unigram_lm_score == 0 \
                else float(lm_score) - float(unigram_lm_score)
            normalized_lm_scores.append(x)
        return normalized_lm_scores

    def calc_lm_scores_normalized_by_len(self) -> List[Union[None, float]]:

        normalized_lm_scores = []
        for lm_score, unigram_lm_score, s in zip(self.lm_scores,
                                                 self.unigram_lm_scores,
                                                 self.sentences):
            x = None \
                if lm_score is None or len(s) == 0 \
                else (float(lm_score) - float(unigram_lm_score)) / len(s)
            normalized_lm_scores.append(x)
        return normalized_lm_scores
