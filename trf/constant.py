from enum import Enum


class Features(Enum):
    TREE_DEPTH = 'tree-depth'
    MODALITY = 'modality'


class DefaultOptions(object):
    KNP = "-dpnd-fast -tab"


HYPERNYM = 'hype'
