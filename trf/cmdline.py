# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import sys
import argparse
import shutil

from trf.syntax import Syntax


def check_executable(executable: str):
    location = shutil.which(executable)
    if location is None:
        print('`{0}` is not found on your PATH.\n'
              'Make sure that `{0}` is installed on your system '
              'and available on the PATH.'.format(executable))
        sys.exit(1)
    else:
        pass


def main():

    executables = ['juman', 'knp']
    for e in executables:
        check_executable(e)

    parser = argparse.ArgumentParser()

    parser.add_argument("-f",
                        "--filename",
                        type=str,
                        help='target text')

    parser.add_argument("--delimiter",
                        type=str,
                        default='。',
                        help='features to calculate')

    args = parser.parse_args()

    text = ''
    if args.filename is not None:
        with open(args.filename, mode='r') as f:
            text = f.read().replace('\n', '')
    else:
        text = sys.stdin.read()

    syntax = Syntax(text, delimiter=args.delimiter)

    print("# 基本指標")
    print("文数：{:d}".format(syntax.n_sentences))
    print("平均文長：{:d}".format(syntax.n_sentences))
    print("トークン数：{:d}".format(syntax.calc_num_of_mrphs()))
    print("タイプ数：{:d}".format(syntax.calc_num_of_types()))

    print("")
    print("# 語彙に基づく指標")
    print("品詞：{:02f}".format(0))
    print("語彙の具体度：{:02f}".format(0))

    print("")
    print("# 統語情報に基づく指標")
    print("仮定節：{:02f}".format(0))
    print("係り受け木の深さ：{:02f}".format(syntax.calc_mean_tree_depth()))

    print("")
    print("# 言語モデルに基づく指標")
    print("言語モデルの尤度：{:02f}".format(0))
    print("容認度：{:02f}".format(0))
