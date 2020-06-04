#!/usr/bin/env bash
set -euo pipefail

# ingest CoNLL files into pickle format
python ingest_conll.py ../data/conll-english/train.txt BIO ../data/conll-english/train.pkl
python ingest_conll.py ../data/conll-english/test.txt BIO ../data/conll-english/test.pkl

# extract Unseen and TCM subsets (Unseen-tokens subset is required to get TCM subsets)
python extract_oov.py any ../data/conll-english/train.pkl ../data/conll-english/test.pkl ../data/conll-english/unseen-any.pkl
python extract_oov.py tokens ../data/conll-english/train.pkl ../data/conll-english/test.pkl ../data/conll-english/unseen-tokens.pkl
python extract_oov.py type ../data/conll-english/train.pkl ../data/conll-english/test.pkl ../data/conll-english/unseen-type.pkl

python extract_tcm.py ../data/conll-english/test.pkl ../data/conll-english/unseen-tokens.pkl ../data/conll-english/TCM.pkl

# Standard Evaluation
python score_oov.py ../data/conll-english/test.txt ../data/conll-english/pred.txt BIO

# Unseen-tokens Evaluation
python score_oov.py ../data/conll-english/test.txt ../data/conll-english/pred.txt BIO \
                    -e ../data/conll-english/unseen-tokens.pkl  -s unseen --schema tokens

# TCM-All Evaluation
python score_tcm.py ../data/conll-english/test.txt ../data/conll-english/pred.txt BIO \
                    -e ../data/conll-english/TCM.pkl -s ambi