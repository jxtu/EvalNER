from typing import List, Union
import attr
import argparse


@attr.s(frozen=True)
class EvalMeta:
    type: str = attr.ib()
    schema: str = attr.ib()
    strategy: str = attr.ib()


@attr.s(frozen=True)
class TypeResult:
    precision: str = attr.ib()
    recall: str = attr.ib()
    fscore: str = attr.ib()
    entityCount: str = attr.ib()
    entityType: str = attr.ib()


@attr.s(frozen=True)
class CoNLLPerformance:
    LOC: TypeResult = attr.ib()
    MISC: TypeResult = attr.ib()
    ORG: TypeResult = attr.ib()
    PER: TypeResult = attr.ib()
    ALL: TypeResult = attr.ib()

    def __str__(self):
        lines = list()
        lines.append(self.LOC.__str__())
        lines.append(self.MISC.__str__())
        lines.append(self.ORG.__str__())
        lines.append(self.PER.__str__())
        lines.append(self.ALL.__str__())
        return "\n".join(lines)


@attr.s(frozen=True)
class OntoPerformance:
    CARDINAL: TypeResult = attr.ib()
    DATE: TypeResult = attr.ib()
    EVENT: TypeResult = attr.ib()
    FAC: TypeResult = attr.ib()
    GPE: TypeResult = attr.ib()
    LANGUAGE: TypeResult = attr.ib()
    LAW: TypeResult = attr.ib()
    LOC: TypeResult = attr.ib()
    MONEY: TypeResult = attr.ib()
    NORP: TypeResult = attr.ib()
    ORDINAL: TypeResult = attr.ib()
    ORG: TypeResult = attr.ib()
    PERCENT: TypeResult = attr.ib()
    PERSON: TypeResult = attr.ib()
    PRODUCT: TypeResult = attr.ib()
    QUANTITY: TypeResult = attr.ib()
    TIME: TypeResult = attr.ib()
    WORK_OF_ART: TypeResult = attr.ib()
    ALL: TypeResult = attr.ib()

    def __str__(self):
        lines = list()
        lines.append(self.CARDINAL.__str__())
        lines.append(self.DATE.__str__())
        lines.append(self.EVENT.__str__())
        lines.append(self.FAC.__str__())
        lines.append(self.GPE.__str__())
        lines.append(self.LANGUAGE.__str__())
        lines.append(self.LAW.__str__())
        lines.append(self.LOC.__str__())
        lines.append(self.MONEY.__str__())
        lines.append(self.NORP.__str__())
        lines.append(self.ORDINAL.__str__())
        lines.append(self.ORG.__str__())
        lines.append(self.PERCENT.__str__())
        lines.append(self.PERSON.__str__())
        lines.append(self.PRODUCT.__str__())
        lines.append(self.QUANTITY.__str__())
        lines.append(self.TIME.__str__())
        lines.append(self.WORK_OF_ART.__str__())
        lines.append(self.ALL.__str__())

        return "\n".join(lines)


@attr.s(auto_attribs=True)
class EvalResult:
    meta: EvalMeta = attr.ib()
    performance: Union[CoNLLPerformance, OntoPerformance] = attr.ib()

    @classmethod
    def from_conll_file(cls, result_input: str) -> "EvalResult":
        with open(result_input, "r") as f:
            lines = f.readlines()
        meta = cls._get_meta(lines)
        loc_res = cls._parse_full(lines[4:8], "LOC")
        misc_res = cls._parse_full(lines[10:14], "MISC")
        org_res = cls._parse_full(lines[16:20], "ORG")
        per_res = cls._parse_full(lines[22:26], "PER")
        all_res = cls._parse_full(lines[28:32], "ALL")
        performance = CoNLLPerformance(loc_res, misc_res, org_res, per_res, all_res)
        return cls(meta, performance)

    @classmethod
    def from_onto_file(cls, result_input: str) -> "EvalResult":
        onto_entity_types = [
            "CARDINAL",
            "DATE",
            "EVENT",
            "FAC",
            "GPE",
            "LANGUAGE",
            "LAW",
            "LOC",
            "MONEY",
            "NORP",
            "ORDINAL",
            "ORG",
            "PERCENT",
            "PERSON",
            "PRODUCT",
            "QUANTITY",
            "TIME",
            "WORK_OF_ART",
            "ALL",
        ]
        results = []
        with open(result_input, "r") as f:
            lines = f.readlines()
        for i, e_type in enumerate(onto_entity_types):
            start_offset = 4 + i * 6
            end_offset = start_offset + 4
            results.append(cls._parse_full(lines[start_offset:end_offset], e_type))
        meta = cls._get_meta(lines)
        performance = OntoPerformance(*results)
        return cls(meta, performance)

    @staticmethod
    def _get_meta(lines: List[str]) -> "EvalMeta":
        parts = lines[0].split(" ")
        eval_type = parts[1]
        eval_schema = parts[-2]
        eval_strategy = lines[1].split(" ")[-2]
        return EvalMeta(eval_type, eval_schema, eval_strategy)

    @staticmethod
    def _parse_full(lines: List[str], e_type: str) -> "TypeResult":
        p = lines[0].strip().split(" ")[-1]
        r = lines[1].strip().split(" ")[-1]
        f1 = lines[2].strip().split(" ")[-1]
        count = lines[3].strip().split(" ")[-1]
        return TypeResult(p, r, f1, count, e_type)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dataset", help="result file from EvalNER", choices=["conll2003", "ontonotes"]
    )
    parser.add_argument("result_file", help="result file from EvalNER")
    args = parser.parse_args()
    if args.dataset == "conll2003":
        eval_result = EvalResult.from_conll_file(args.result_file)
    else:
        eval_result = EvalResult.from_onto_file(args.result_file)
    print(eval_result.meta)
    print(eval_result.performance)


if __name__ == "__main__":
    main()
