from __future__ import print_function

import argparse

from trf.contant import Features
from trf.syntax import Syntax


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--text",
                        type=str,
                        help='target text')

    parser.add_argument("--features",
                        type=str,
                        nargs='+',
                        choices=[f.value for f in list(Features)],
                        required=True,
                        help='features to calculate')

    parser.add_argument("--delimiter",
                        type=str,
                        default='\n',
                        help='features to calculate')

    args = parser.parse_args()
    features = list(map(lambda f: Features(f), args.features))

    if Features.TREE_DEPTH in features:
        syntax = Syntax(args.text, delimiter=args.delimiter)
        print("Mean Tree Depth: {:02f}".format(syntax.calc_mean_tree_depth()))
