from typing import List
import sys
import numpy as np

from sqlalchemy import Column, String, Integer, and_
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session, sessionmaker

from trf.constant import HYPERNYM


Base = declarative_base()


class Word(Base):

    __tablename__ = 'word'

    wordid = Column(String, primary_key=True)
    lang = Column(String)
    lemma = Column(String)
    pron = Column(String)
    pos = Column(String)


class Sense(Base):

    __tablename__ = 'sense'

    synset = Column(String, primary_key=True)
    wordid = Column(Integer, primary_key=True)
    lang = Column(String)
    rank = Column(String)
    lexid = Column(Integer)
    freq = Column(Integer)
    src = Column(String)


class Synlink(Base):

    __tablename__ = 'synlink'

    synset1 = Column(String, primary_key=True)
    synset2 = Column(String)
    link = Column(String, primary_key=True)
    src = Column(String)


class WordNet:

    def __init__(self, db_path: str, lang: str):

        engine = create_engine('sqlite:///{}'.format(db_path))
        SessionMaker = sessionmaker(bind=engine)
        self.session = SessionMaker()
        self.lang = lang

    def traverse(self, senses: List[Sense], depth: int) -> int:

        if senses:
            synsets = [sense.synset for sense in senses]
            synlinks = self.session \
                .query(Synlink) \
                .filter(and_(Synlink.synset1.in_(synsets),
                             Synlink.link == HYPERNYM)) \
                .all()
            if synlinks:
                synset2s = [synlink.synset2 for synlink in synlinks]
                child_senses = self.session \
                    .query(Sense) \
                    .filter(and_(Sense.synset.in_(synset2s),
                                 Sense.lang == self.lang)) \
                    .all()
                return self.traverse(child_senses, depth + 1)
            else:
                return depth
        else:
            return depth

    def calc_mean_thesaurus_depths(self, surfaces: List[str]) -> float:
        """
        Parameters:
            session
            surface_list: 分析対象のテキスト中の単語リスト(一般名詞のみ)
        """

        if surfaces is None or len(surfaces) == 0:
            return 0.0

        depths = []
        for surface in surfaces:

            word = self.session \
                .query(Word) \
                .filter(Word.lemma == surface) \
                .first()

            if word:
                senses = self.session \
                    .query(Sense) \
                    .filter(Sense.wordid == word.wordid) \
                    .all()

                depth = self.traverse(senses, 0)
                depths.append(depth)
            else:
                continue

        return np.mean(depths) if depths else 0.0
