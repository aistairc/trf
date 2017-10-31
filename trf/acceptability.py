from typing import Dict, List, Tuple, Union
import math


class Acceptability:

    def __init__(self,
                 rnnlm_output_filename: str,
                 wordfreq_filename: str,
                 sentence_filename: str):

        self.lmscores = self._load_lmscores(rnnlm_output_filename)

        self.word_freq, self.n_total_words = \
            self._load_word_freq(wordfreq_filename, threshold=1)

        self.sentences = self._load_sentences(sentence_filename)

        self.sentence_lengths = [len(s.strip().split()) for s in self.sentences]

        self.unigram_lmscores = \
            self._calc_unigram_lmscores(self.sentences,
                                        self.word_freq,
                                        self.n_total_words)

    @staticmethod
    def _load_lmscores(rnnlm_output_filename: str) -> List[Union[None, float]]:
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

    @staticmethod
    def _load_sentences(filename: str) -> List[str]:
        with open(filename, mode='r') as f:
            return [line.rstrip() for line in f]

    @staticmethod
    def _calc_unigram_lmscores(sentences: List[str],
                               word_freq: Dict[str, int],
                               n_total_words: int) -> List[float]:

        unigram_scores = []
        for s in sentences:
            unigram_score = 0.0

            for word in s.split():
                n = float(n_total_words)
                x = float(word_freq.get(word, word_freq['<unk/>']))
                unigram_score += math.log(x / n)

            unigram_scores.append(unigram_score)

        return unigram_scores
