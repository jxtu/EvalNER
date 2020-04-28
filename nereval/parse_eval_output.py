from typing import List
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
class Performance:
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


@attr.s(auto_attribs=True)
class EvalResult:
    meta: EvalMeta = attr.ib()
    performance: Performance = attr.ib()

    @classmethod
    def from_file(cls, result_input: str) -> "EvalResult":
        with open(result_input, "r") as f:
            lines = f.readlines()
        meta = cls._get_meta(lines)
        loc_res = cls._parse_full(lines[4:8], "LOC")
        misc_res = cls._parse_full(lines[10:14], "MISC")
        org_res = cls._parse_full(lines[16:20], "ORG")
        per_res = cls._parse_full(lines[22:26], "PER")
        all_res = cls._parse_full(lines[28:32], "ALL")
        performance = Performance(loc_res, misc_res, org_res, per_res, all_res)
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
    parser.add_argument("result_file", help="result file from EvalNER")
    args = parser.parse_args()
    eval_result = EvalResult.from_file(args.result_file)
    print(eval_result.meta)
    print(eval_result.performance)


if __name__ == "__main__":
    main()
