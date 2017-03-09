# -*- encoding: utf-8 -*-

from __future__ import unicode_literals


def split_text(text, delimiter='\n'):
    """
    Args:
        text (str)
        delimiter (str)
    Returns:
        list(str)
    """

    sentences = text.split(delimiter)
    if len(sentences[-1]) == 0:
        return sentences[:-1]
    else:
        return sentences
