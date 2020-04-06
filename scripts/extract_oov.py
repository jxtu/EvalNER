import collections
import argparse
import sys
from typing import Set
sys.path.append('../')
from nerpy import Document
from nerpy import load_pickled_documents, pickle_obj


def entity_dist(docs: [Document]) -> Set:
    ent_counter = collections.Counter()
    for doc in docs:
        ent_counter.update((mention.tokenized_text(doc), mention.entity_type) for mention in doc.mentions)
    return set(ent_counter.keys())


def extract_oov(
        train_docs: [Document], test_docs: [Document], output_path: str
) -> None:
    train_ents = entity_dist(train_docs)
    test_ents = entity_dist(test_docs)
    unseen = test_ents - train_ents
    seen = test_ents - unseen
    pickled = {'seen': seen, 'unseen': unseen}
    pickle_obj(pickled, output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("train_pkl", help="training docs pickle file")
    parser.add_argument("test_pkl", help="test docs pickle file")

    parser.add_argument("output", help="output entities pickle file")
    args = parser.parse_args()
    train_docs = load_pickled_documents(args.train_pkl)
    print(f"Loading data from {args.train_pkl}")
    test_docs = load_pickled_documents(args.test_pkl)
    print(f"Loading data from {args.test_pkl}")
    extract_oov(train_docs, test_docs, args.output)
    print(f"Wrote output to {args.output}")


if __name__ == "__main__":
    main()

