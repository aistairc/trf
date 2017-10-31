#!/bin/bash

tools="$(pwd)/tools"
juman_uri="http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2"
knp_uri="http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.18.tar.bz2"
pyknp_uri="http://nlp.ist.i.kyoto-u.ac.jp/DLcounter/lime.cgi?down=http://lotus.kuee.kyoto-u.ac.jp/nl-resource/pyknp/pyknp-0.3.tar.gz"
juman_prefix="${tools}"

exists() {
    command -v "$1" > /dev/null 2>&1
}

export PATH="$PATH:${tools}/bin"

if exists juman
then
    juman_location="$(which juman)"
    juman_prefix=$(dirname $juman_location)
    echo "Juman is installed"
else
    mkdir -p tools/tmp
    juman_archive="$(basename $juman_uri)"
    wget --no-clobber $juman_uri -O "${tools}/tmp/${juman_archive}"
    tar -xkf "${tools}/tmp/${juman_archive}" -C "${tools}/tmp" > /dev/null 2>&1
    cd "${tools}/tmp/$(basename ${juman_archive} '.tar.bz2')"
    ./configure --prefix="${tools}"
    make
    make install
fi

if exists knp
then
    echo "KNP is installed"
else
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
