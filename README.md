# EvalNER
This is the code base for the EMNLP 2020 submission: _Evaluating Tough Mentions to Better Understand NER Performance_.
All scripts should be run from the directory where the script locates. All scripts mentioned can be found in `nereval/`. `demo.sh` is provided to demonstrate the whole evaluation process.
## Data Preparation
NER datasets and corresponding prediction file on its test set. All files need to be of CoNLL format, i.e. set your directory like this:
```
├── data
│   ├── conll-english         # CoNLL 2003 English dataset
│   │   ├── train.txt
│   │   ├── valid.txt
│   │   ├── test.txt
│   │   └── pred.txt        # prediction file on test.txt
``` 
## Entity Mentions Subsets
Unseen/TCM subsets need to be generated first before running the scorer.
- Run `ingest_conll.py` to get pickled `train.txt` and `test.txt`. 
- Run `extract_tcm.py` and `extract_oov.py` to pickle unseen and type-confusable mention subsets.

## Evaluation
- Run `score_oov.py` to get per-type performance on different Unseen mention subsets.
- Run `score_tcm.py` to get per-type performance on different type-confusable mention subsets.