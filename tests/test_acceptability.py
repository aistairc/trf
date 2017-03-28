from __future__ import division, unicode_literals
import os, sys
from pathlib import Path
print(Path().resolve().parent)
sys.path.append(Path().resolve().parent)
from acceptability import Acceptability

def main():

    accep = Acceptability("rnnlm.output", "uniq.dat", "test.input")



if __name__ == "__main__":
    main()
