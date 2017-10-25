#!/bin/bash

#日本語Wordnet
jwordnet="http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz"
db="$(basename $jwordnet)"

if [ ! -d data ]
then
    mkdir data
fi

if [ ! -f "data/$db" ]
then
    wget -O data/$db $jwordnet
fi

if [ ! -f "data/${db%.*}" ]
then
    gunzip --keep "data/${db%.*}"
fi
