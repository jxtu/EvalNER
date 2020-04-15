#!/usr/bin/env bash
set -euo pipefail

# OOV evaluation
# schema: full
python score_oov.py ../data/conll2003/test.txt ../data/preds/wordlstm_charcnn_crf.pred BIO \
                    -e ../data/ents/full_OOV.pkl  -s unseen --schema full

# schema: token
python score_oov.py ../data/conll2003/test.txt ../data/preds/wordlstm_charcnn_crf.pred BIO \
                    -e ../data/ents/token_OOV.pkl -s unseen --schema token

# schema: type
python score_oov.py ../data/conll2003/test.txt ../data/preds/wordlstm_charcnn_crf.pred BIO \
                    -e ../data/ents/type_OOV.pkl  -s unseen --schema type



# TCE evaluation
python score_tce.py ../data/conll2003/test.txt ../data/preds/wordlstm_charcnn_crf.pred BIO \
                    -e ../data/ents/TCE.pkl -s ambi