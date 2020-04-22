#!/usr/bin/env bash
set -euo pipefail

MODEL=$1

mkdir ../data/output/"${MODEL}"

# Standard Evaluation
python score_oov.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO > ../data/output/"${MODEL}"/standard.txt

# OOV evaluation
# schema: full
python score_oov.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO \
                    -e ../data/ents/full_OOV.pkl  -s unseen --schema full > ../data/output/"${MODEL}"/oov_full.txt
# schema: token
python score_oov.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO \
                    -e ../data/ents/token_OOV.pkl -s unseen --schema token > ../data/output/"${MODEL}"/oov_token.txt
# schema: type
python score_oov.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO \
                    -e ../data/ents/type_OOV.pkl  -s unseen --schema type > ../data/output/"${MODEL}"/oov_type.txt


# TCE evaluation
# schema: ambi
python score_tce.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO \
                    -e ../data/ents/TCE.pkl -s ambi > ../data/output/"${MODEL}"/tce_ambi.txt
# schema: seen_ambi
python score_tce.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO \
                    -e ../data/ents/TCE.pkl -s seen_ambi > ../data/output/"${MODEL}"/tce_seen_ambi.txt
# schema: unseen_ambi
python score_tce.py ../data/conll2003/test.txt ../data/experiments_preds/"${MODEL}".pred BIO \
                    -e ../data/ents/TCE.pkl -s unseen_ambi > ../data/output/"${MODEL}"/tce_unseen_ambi.txt