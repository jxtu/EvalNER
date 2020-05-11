from typing import Tuple, List, Optional, Dict
from collections import defaultdict
import attr

from nerpy import load_pickled_documents
from nerpy import Document, Mention

from orderedset import OrderedSet


@attr.s(auto_attribs=True)
class EntityInspector:
    documents: List[Document] = attr.ib()

    @classmethod
    def from_pickle(cls, pickle_file: str) -> "EntityInspector":
        documents: List["Document"] = load_pickled_documents(pickle_file)
        return cls(documents)

    def __call__(self, doc_idx: int) -> Tuple[Tuple[str, str]]:
        doc = self.documents[doc_idx]
        entities = tuple(self._simplify_mention(doc, mention) for mention in doc.mentions)
        return entities

    def get_all_entities(self) -> Dict[str, "OrderedSet"]:
        entities_dict = defaultdict(OrderedSet)
        for doc in self.documents:
            for mention in doc.mentions:
                entities_dict[mention.entity_type.types[0]].add(
                    mention.tokenized_text(doc)
                )
        return entities_dict

    @staticmethod
    def _simplify_mention(doc: "Document", mention: "Mention") -> Tuple[str, str]:
        return mention.tokenized_text(doc), mention.entity_type.types[0]


if __name__ == "__main__":
    pkl_file = "../data/ontonotes/test.pkl"
    ents_inspector = EntityInspector.from_pickle(pkl_file)
    all_ents = ents_inspector.get_all_entities()
    for e_type in all_ents:
        with open(f"../data/ents/ontonotes/{e_type}.txt", "w") as f:
            f.write("\n".join(all_ents[e_type]))
