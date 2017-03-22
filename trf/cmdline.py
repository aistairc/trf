# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import argparse

from trf.syntax import Syntax


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-f",
                        "--filename",
                        type=str,
                        help='target text')

    parser.add_argument("--no-knp",
                        type=str,
                        help='run without KNP')

    parser.add_argument("--delimiter",
                        type=str,
                        default='\n',
                        help='features to calculate')

    args = parser.parse_args()

    text = ''
    if args.filename is not None:
        with open(args.filename, mode='r') as f:
            text = f.read().replace('\n', '')
    elif sys.stdin.isatty():
        text = sys.stdin.read()

    syntax = Syntax(text, delimiter=args.delimiter)
    print("Number of Sentences: {:d}".format(syntax.n_sentences))
    print("Mean Tree Depth: {:02f}".format(syntax.calc_mean_tree_depth()))
