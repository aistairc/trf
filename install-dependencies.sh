#!/bin/bash

project_root="$(pwd)"

tools="$(pwd)/tools"
juman_uri="http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2"
knp_uri="http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.18.tar.bz2"
pyknp_uri="http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://lotus.kuee.kyoto-u.ac.jp/nl-resource/pyknp/pyknp-0.3.tar.gz"
juman_prefix="${tools}"
rnnlm_model_uri="https://s3-ap-northeast-1.amazonaws.com/plu-aist/trf/jawiki-20160818-100M-words"
rnnlm_model="$(basename ${rnnlm_model_uri})"

exists() {
    command -v "$1" > /dev/null 2>&1
}

export PATH="$PATH:${tools}/bin"

if (exists juman) && (exists knp)
then
    echo "Juman is installed"
    echo "KNP is installed"
else
    mkdir -p tools/tmp
    juman_archive="$(basename $juman_uri)"
    wget --no-clobber $juman_uri -O "${tools}/tmp/${juman_archive}"
    tar -xkf "${tools}/tmp/${juman_archive}" -C "${tools}/tmp" > /dev/null 2>&1
    cd "${tools}/tmp/$(basename ${juman_archive} '.tar.bz2')"
    ./configure --prefix="${tools}"
    make
    make install

    mkdir -p tools/tmp
    knp_archive="$(basename $knp_uri)"
    wget --no-clobber $knp_uri -O "${tools}/tmp/${knp_archive}"
    tar -xkf "${tools}/tmp/${knp_archive}" -C "${tools}/tmp" > /dev/null 2>&1
    cd "${tools}/tmp/$(basename ${knp_archive} '.tar.bz2')"
    ./configure --prefix="${tools}" --with-juman-prefix="${juman_prefix}"
    make
    make install
fi

if python -c 'import pyknp' > /dev/null 2>&1
then
    echo "PyKNP is installed"
else
    pyknp_archive="$(basename $pyknp_uri)"
    wget --no-clobber $pyknp_uri -O "${tools}/tmp/${pyknp_archive}"
    tar -xkf "${tools}/tmp/${pyknp_archive}" -C "${tools}/tmp" > /dev/null 2>&1
    pip install "${tools}/tmp/$(basename ${pyknp_archive} '.tar.gz')"
fi

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

if exists rnnlm
then
    echo "RNNLM is installed"
else
    if [ ! -d ${tools}/tmp/faster-rnnlm ]
    then
         git clone https://github.com/yandex/faster-rnnlm.git ${tools}/tmp/faster-rnnlm
    fi
    cd ${tools}/tmp/faster-rnnlm/faster-rnnlm
    sed -i.bak -e 's/^\s*NVCC_CFLAGS = -O3 -march=native -funroll-loops$/NVCC_CFLAGS = -O3 -march=native -funroll-loops -D_FORCE_INLINES/' Makefile
    make
    cd $project_root
    ln -sf ${tools}/tmp/faster-rnnlm/faster-rnnlm/rnnlm tools/bin/rnnlm
fi

pip install -r "${project_root}/requirements.txt"

if [ ! -f data/$rnnlm_model ]
then
    wget $rnnlm_model_uri -O data/$(basename ${rnnlm_model_uri})
fi

if [ ! -f "data/${rnnlm_model}.nnet" ]
then
    wget "${rnnlm_model_uri}.nnet" -O "data/$(basename ${rnnlm_model_uri}).nnet"
fi
