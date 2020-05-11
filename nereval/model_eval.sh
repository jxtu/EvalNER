#!/usr/bin/env bash
set -euo pipefail

MODEL=$1
CORPUS=$2

mkdir ../data/output/"${CORPUS}"/"${MODEL}"

echo "Standard Evaluation..."
# Standard Evaluation
python score_oov.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    > ../data/output/"${CORPUS}"/"${MODEL}"/standard.txt

echo "OOV Evaluation..."
# OOV evaluation
# schema: full
python score_oov.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    -e ../data/ents/"${CORPUS}"/full_OOV.pkl  -s unseen --schema full > ../data/output/"${CORPUS}"/"${MODEL}"/oov_full.txt
# schema: token
python score_oov.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    -e ../data/ents/"${CORPUS}"/token_OOV.pkl -s unseen --schema token > ../data/output/"${CORPUS}"/"${MODEL}"/oov_token.txt
# schema: type
python score_oov.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    -e ../data/ents/"${CORPUS}"/type_OOV.pkl  -s unseen --schema type > ../data/output/"${CORPUS}"/"${MODEL}"/oov_type.txt

echo "TCE Evaluation..."
# TCE evaluation
# schema: ambi
python score_tce.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    -e ../data/ents/"${CORPUS}"/TCE.pkl -s ambi > ../data/output/"${CORPUS}"/"${MODEL}"/tce_ambi.txt
# schema: seen_ambi
python score_tce.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    -e ../data/ents/"${CORPUS}"/TCE.pkl -s seen_ambi > ../data/output/"${CORPUS}"/"${MODEL}"/tce_seen_ambi.txt
# schema: unseen_ambi
python score_tce.py ../data/"${CORPUS}"/test_one_doc.txt ../data/experiments_preds/"${CORPUS}"/"${MODEL}".pred BIO \
                    -e ../data/ents/"${CORPUS}"/TCE.pkl -s unseen_ambi > ../data/output/"${CORPUS}"/"${MODEL}"/tce_unseen_ambi.txt