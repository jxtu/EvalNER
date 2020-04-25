from typing import List, NamedTuple
import argparse


class EvalMeta(NamedTuple):
    type: str
    schema: str
    strategy: str


class TypeResult(NamedTuple):
    precision: str
    recall: str
    fscore: str
    entityCount: str
    entityType: str


class Performance(NamedTuple):
    LOC: NamedTuple
    MISC: NamedTuple
    ORG: NamedTuple
    PER: NamedTuple
    ALL: NamedTuple


class EvalParser(object):
    def __init__(self, result_input: str):
        with open(result_input, "r") as f:
            result_lines = f.readlines()
        self.meta = self._get_meta(result_lines[:2])
        loc_res = self._parse_full(result_lines[4:8], "LOC")
        misc_res = self._parse_full(result_lines[10:14], "MISC")
        org_res = self._parse_full(result_lines[16:20], "ORG")
        per_res = self._parse_full(result_lines[22:26], "PER")
        all_res = self._parse_full(result_lines[28:32], "ALL")
        self.performance = Performance(loc_res, misc_res, org_res, per_res, all_res)

    @staticmethod
    def _get_meta(lines: List[str]):
        parts = lines[0].split(" ")
        eval_type = parts[1]
        eval_schema = parts[-2]
        eval_strategy = lines[1].split(" ")[-2]
        return EvalMeta(eval_type, eval_schema, eval_strategy)

    @staticmethod
    def _parse_full(lines: List[str], e_type: str):
        p = lines[0].strip().split(" ")[-1]
        r = lines[1].strip().split(" ")[-1]
        f1 = lines[2].strip().split(" ")[-1]
        count = lines[3].strip().split(" ")[-1]
        return TypeResult(p, r, f1, count, e_type)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("result_file", help="result file from EvalNER")
    args = parser.parse_args()
    eval_parser = EvalParser(args.result_file)
    print(eval_parser.meta)
    for t in eval_parser.performance:
        print(t)


if __name__ == "__main__":
    main()
