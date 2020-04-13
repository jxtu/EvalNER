import collections
import argparse
import sys
from typing import Set
sys.path.append('../')
from nerpy import Document
from nerpy import load_pickled_documents, pickle_obj


def full_entity_dist(docs: [Document]) -> Set:
    ent_counter = collections.Counter()
    for doc in docs:
        ent_counter.update((mention.tokenized_text(doc), mention.entity_type) for mention in doc.mentions)
    return set(ent_counter.keys())


def token_entity_dist(docs: [Document]) -> Set:
    ent_counter = collections.Counter()
    for doc in docs:
        ent_counter.update((mention.tokenized_text(doc)) for mention in doc.mentions)
    return set(ent_counter.keys())


def type_entity_dist(docs: [Document]) -> Set:
    ent_counter = collections.Counter()
    for doc in docs:
        ent_counter.update((mention.tokenized_text(doc), mention.entity_type) for mention in doc.mentions)
    return set(ent_counter.keys())


def extract_oov(
        strategy: str, train_docs: [Document], test_docs: [Document], output_path: str
) -> None:
    if strategy is 'full':
        train_ents = full_entity_dist(train_docs)
        test_ents = full_entity_dist(test_docs)
        unseen = test_ents - train_ents
        seen = test_ents - unseen
    elif strategy == 'token':
        train_ents = token_entity_dist(train_docs)
        test_ents = token_entity_dist(test_docs)
        unseen = test_ents - train_ents
        seen = test_ents - unseen
    elif strategy == 'type':
        train_ents = full_entity_dist(train_docs)
        test_ents = full_entity_dist(test_docs)
        train_ents_tokens = token_entity_dist(train_docs)
        test_type_ents = set(pair for pair in test_ents if pair[0] in train_ents_tokens)
        unseen = test_type_ents - train_ents
        seen = test_ents - unseen
    else:
        raise KeyError(f'Cannot find strategy: {strategy}')
    pickled = {'seen': seen, 'unseen': unseen}
    pickle_obj(pickled, output_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("strategy", help="oov comparison strategy", choices=['full', 'token', 'type'])
    parser.add_argument("train_pkl", help="training docs pickle file")
    parser.add_argument("test_pkl", help="test docs pickle file")
    parser.add_argument("output", help="output entities pickle file")
    args = parser.parse_args()
    train_docs = load_pickled_documents(args.train_pkl)
    print(f"Loading data from {args.train_pkl}")
    test_docs = load_pickled_documents(args.test_pkl)
    print(f"Loading data from {args.test_pkl}")
    print(f'Using strategy: {args.strategy}')
    extract_oov(args.strategy, train_docs, test_docs, args.output)
    print(f"Writing output to {args.output}")


if __name__ == "__main__":
    main()

