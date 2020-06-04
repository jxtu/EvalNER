import collections
import argparse
import sys
from typing import Set, Tuple, Dict

sys.path.append("../")
from nerpy import Document
from nerpy import load_pickled_documents, load_pickled_obj, pickle_obj


def get_ambi_entity(docs: [Document]) -> Tuple[Set, ...]:
    ent_dist = collections.defaultdict(dict)
    ambi_ents = set()
    unambi_ents = set()
    for doc in docs:
        for mention in doc.mentions:
            ent_dist[mention.tokenized_text(doc)][mention.entity_type] = (
                mention.tokenized_text(doc),
                mention.entity_type,
            )
    for ent in ent_dist:
        if len(ent_dist[ent]) > 1:
            ambi_ents.add(ent)
        else:
            unambi_ents.add(ent)

    return ambi_ents, unambi_ents


def extract_tce(
    test_docs: [Document], oov_ents: Dict[str, Set], output_path: str
) -> None:
    ambi_ents, unambi_ents = get_ambi_entity(test_docs)
    seen_ambi = ambi_ents & oov_ents["seen"]
    seen_unambi = oov_ents["seen"] - seen_ambi
    unseen_ambi = ambi_ents & oov_ents["unseen"]
    unseen_unambi = oov_ents["unseen"] - unseen_ambi
    pickled = {
        "seen_ambi": seen_ambi,
        "seen_unambi": seen_unambi,
        "unseen_ambi": unseen_ambi,
        "unseen_unambi": unseen_unambi,
    }
    pickle_obj(pickled, output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("test_pkl", help="test docs pickle file")
    parser.add_argument("oov_pkl", help="Unseen-tokens mentions pickle file")
    parser.add_argument("output", help="output entities pickle file")
    args = parser.parse_args()
    test_docs = load_pickled_documents(args.test_pkl)
    oov_ents = load_pickled_obj(args.oov_pkl)
    print(f"Loading data from {args.test_pkl}")
    extract_tce(test_docs, oov_ents, args.output)
    print(f"Writing output to {args.output}")


if __name__ == "__main__":
    main()
