#!/usr/bin/env bash
set -euo pipefail

# add document separators to conll files for fast evaluation
python sentence2doc.py ../data/test.conll ../data/test_docs.conll

# output Evaluation result and latex table
python score_oov.py ../data/test_docs.conll ../data/out_docs.txt BIO

# sample output

#===== OOV Evaluation Schema: None =====
#----- Evaluation Strategy: Standard -----
#***** Entity Type Scores *****
#Entity Type: MEDICAL_OBJECT
#Precision: 34.74
#Recall: 47.44
#F1-score: 40.11
#Entity Count: 917
#
#Entity Type: MEDICATION
#Precision: 85.34
#Recall: 90.55
#F1-score: 87.87
#Entity Count: 12385
#
#Entity Type: PROBLEM
#Precision: 76.83
#Recall: 80.21
#F1-score: 78.49
#Entity Count: 59795
#
#Entity Type: TEST
#Precision: 78.89
#Recall: 78.10
#F1-score: 78.50
#Entity Count: 16741
#
#Entity Type: TREATMENT_PROCEDURE
#Precision: 54.96
#Recall: 62.89
#F1-score: 58.66
#Entity Count: 4387
#
#***** Overall Score *****
#Total Precision: 76.67
#Total Recall:  80.07
#Total F1-Score: 78.33
#Total Count: 94225
#
#
# \begin{tabular}{llllr}
#\toprule
#{} & Precision & Recall &     F1 &  Count \\
#\midrule
#PROBLEM             &     34.74 &  47.44 &  40.11 &    917 \\
#MEDICATION          &     85.34 &  90.55 &  87.87 &  12385 \\
#TEST                &     76.83 &  80.21 &  78.49 &  59795 \\
#TREATMENT\_PROCEDURE &     78.89 &  78.10 &  78.50 &  16741 \\
#MEDICAL\_OBJECT      &     54.96 &  62.89 &  58.66 &   4387 \\
#ALL                 &     76.67 &  80.07 &  78.33 &  94225 \\
#\bottomrule
#\end{tabular}
