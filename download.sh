#!/bin/bash

project_root="$(pwd)"

jwordnet="http://compling.hss.ntu.edu.sg/wnja/data/1.1/wnjpn.db.gz"
db="$(basename $jwordnet)"

if [ ! -d data ]
then
    mkdir data
fi

if [ ! -f "data/$db" ]
then
    wget --quiet -O data/$db $jwordnet
fi

if [ ! -f "data/${db%.*}" ]
then
    gunzip --keep "data/${db%.*}"
fi

if [ -x faster-rnnlm/faster-rnnlm/rnnlm ]
then
    echo "RNNLM is installed"
else
    git clone https://github.com/yandex/faster-rnnlm.git
    cd faster-rnnlm
    git checkout "c35e481d7d890aebd7667b0bab6681bc2bcdef20"
    ./build.sh
    cd ${project_root}
fi

rnnlm_model_uri="https://s3-ap-northeast-1.amazonaws.com/plu-aist/trf/jawiki-20160818-100M-words"
rnnlm_model="$(basename ${rnnlm_model_uri})"

if [ ! -f "data/$rnnlm_model" ]
then
    wget --quiet $rnnlm_model_uri -O data/$(basename ${rnnlm_model_uri})
fi

if [ ! -f "data/${rnnlm_model}.nnet" ]
then
    wget --quiet "${rnnlm_model_uri}.nnet" -O "data/$(basename ${rnnlm_model_uri}).nnet"
fi
