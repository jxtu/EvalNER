#! /usr/bin/env python

import argparse
import os
import sys
sys.path.append('../')

from nerpy import SUPPORTED_ENCODINGS, CoNLLIngester, get_mention_encoder, score_prf, load_pickled_obj


def score_oov(
    reference_path: str, prediction_path: str, schema: str, external_ents_path: str,
        encoding_name: str, eval_strategy: str, ignore_comments: bool
) -> None:
    encoder = get_mention_encoder(encoding_name)

    with open(reference_path, encoding="utf8") as reference_file:
        reference_docs = CoNLLIngester(encoder(), ignore_comments=ignore_comments).ingest(
            reference_file, os.path.basename(reference_path)
        )

    with open(prediction_path, encoding="utf8") as prediction_file:
        pred_docs = CoNLLIngester(encoder(), ignore_comments=ignore_comments).ingest(
            prediction_file, os.path.basename(prediction_path)
        )

    print(f'===== OOV Evaluation Schema: {schema} =====')

    if not external_ents_path:
        print(f'----- Evaluation Strategy: Standard -----')
        res = score_prf(reference_docs, pred_docs, schema)
    else:
        ents_dict = load_pickled_obj(external_ents_path)
        print(f'----- Evaluation Strategy: {eval_strategy} -----')
        if eval_strategy == 'seen':
            external_ents = ents_dict['unseen']
        elif eval_strategy == 'unseen':
            external_ents = ents_dict['seen']
        else:
            external_ents = set()
            print(f'cannot identify eval strategy: {eval_strategy}, use standard evaluation')
        res = score_prf(reference_docs, pred_docs, schema, external_ents)
    print(res)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CoNLL")
    parser.add_argument(
        "reference_file", help="reference (correct results) CoNLL format file"
    )
    parser.add_argument(
        "prediction_file", help="predicted (system output) CoNLL format file"
    )
    parser.add_argument(
        "mention_encoding", help="mention encoding of files", choices=SUPPORTED_ENCODINGS
    )
    parser.add_argument(
        "-e", "--external_ents", help="external entities pickle file")

    parser.add_argument(
        "--schema", help="OOV evaluation schema, e.g. full or token", choices=['full', 'token', 'type']
    )
    parser.add_argument(
        "-s", "--eval_strategy", help="evaluation strategy, e.g. seen or unseen"
    )

    parser.add_argument(
        "--ignore-comments", action="store_true", help="ignore comment lines"
    )
    args = parser.parse_args()

    score_oov(
        args.reference_file,
        args.prediction_file,
        args.schema,
        args.external_ents,
        args.mention_encoding,
        args.eval_strategy,
        args.ignore_comments,
    )


if __name__ == "__main__":
    main()
