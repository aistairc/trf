# -*- encoding: utf-8 -*-


def split_text(text, delimiter='\n'):
    """
    Args:
        text (str)
        delimiter (str)
    Returns:
        list(str)
    """
    return [s.strip() for s in text.split(delimiter) if len(s) > 0]
