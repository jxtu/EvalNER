#! /usr/bin/env python

import argparse
import os
import sys

sys.path.append("../")

from nerpy import (
    SUPPORTED_ENCODINGS,
    CoNLLIngester,
    get_mention_encoder,
    tce_score_prf,
    load_pickled_obj,
)


def score_tce(
    reference_path: str,
    prediction_path: str,
    external_ents_path: str,
    encoding_name: str,
    eval_strategy: str,
    ignore_comments: bool,
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

    print(f"===== TCE Evaluation =====")

    if not external_ents_path:
        print(f"----- Evaluation Strategy: Standard -----")
        res = tce_score_prf(reference_docs, pred_docs)
    else:
        ents_dict = load_pickled_obj(external_ents_path)
        print(f"----- Evaluation Strategy: {eval_strategy} -----")
        if eval_strategy == "ambi":
            external_ents = ents_dict["unambi"]
        elif eval_strategy == "unambi":
            external_ents = ents_dict["ambi"]
        else:
            external_ents = set()
            print(
                f"cannot identify eval strategy: {eval_strategy}, use standard evaluation"
            )
        res = tce_score_prf(reference_docs, pred_docs, external_ents)
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
    parser.add_argument("-e", "--external_ents", help="external entities pickle file")

    parser.add_argument(
        "-s",
        "--eval_strategy",
        help="evaluation strategy, e.g. ambi or unambi",
        choices=["ambi", "unambi"],
    )

    parser.add_argument(
        "--ignore-comments", action="store_true", help="ignore comment lines"
    )
    args = parser.parse_args()

    score_tce(
        args.reference_file,
        args.prediction_file,
        args.external_ents,
        args.mention_encoding,
        args.eval_strategy,
        args.ignore_comments,
    )


if __name__ == "__main__":
    main()
