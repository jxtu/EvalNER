from os.path import join as pjoin
import pandas as pd
from nereval.parse_eval_output import EvalResult
from nerpy import ScoringResult
from decimal import ROUND_HALF_UP, Context, Decimal


# def get_recall(input_file):
#     ep = EvalResult.from_file(input_file)
#     return ep.performance.ALL.recall
#
#
# def get_prf1(input_file):
#     ep = EvalResult.from_file(input_file)
#     return ep.performance.ALL


# output_path = "../data/output"
# folder_lst = ["charcnn_wordcnn_crf", "wordlstm_charcnn_crf", "BERT", "stanza", "flair"]
# oov_file_lst = ["standard.txt", "oov_token.txt", "oov_full.txt", "oov_type.txt"]
# tce_file_lst = [
#     "standard.txt",
#     "tce_ambi.txt",
#     "tce_seen_ambi.txt",
#     "tce_unseen_ambi.txt",
# ]

# recalls = []
# #
# for folder in folder_lst:
#     recall_values = [get_recall(pjoin(output_path, pjoin(folder, file))) for file in tce_file_lst]
#     recalls.append(recall_values)
#
# recall_df = pd.DataFrame(recalls, index=folder_lst, columns=tce_file_lst)
# print(recall_df.to_latex())

# results = []
# for folder in folder_lst:
#     res = get_prf1(pjoin(output_path, pjoin(folder, "standard.txt")))
#     recall = res.recall
#     precision = res.precision
#     fscore = res.fscore
#     results.append([precision, recall, fscore])
#
# results_df = pd.DataFrame(results, index=folder_lst, columns=["Precision", "Recall", "F1"])
# print(results_df.to_latex())

# all_counts = []
# for file in oov_file_lst + tce_file_lst:
#     ep = EvalResult.from_file(pjoin(output_path, pjoin("flair", file)))
#     p = ep.performance
#     counts = [
#         p.LOC.entityCount,
#         p.ORG.entityCount,
#         p.PER.entityCount,
#         p.MISC.entityCount,
#         p.ALL.entityCount,
#     ]
#     all_counts.append(counts)
#
# all_counts_df = pd.DataFrame(
#     all_counts, index=oov_file_lst + tce_file_lst, columns="LOC ORG PER MISC ALL".split()
# )
# print(all_counts_df.to_latex())
# ress = []
# for folder in ["flair"]:
#     for file in ["standard.txt", "oov_type.txt", "tce_ambi.txt", "tce_seen_ambi.txt", "tce_unseen_ambi.txt"]:
#         ep = EvalResult.from_file(pjoin(output_path, pjoin(folder, file)))
#         p = ep.performance
#         res = [p.LOC.recall, p.ORG.recall, p.PER.recall, p.MISC.recall, p.ALL.recall]
#         ress.append(res)
# ress_df = pd.DataFrame(ress, index=["standard.txt", "oov_type.txt", "tce_ambi.txt", "tce_seen_ambi.txt",
#                                     "tce_unseen_ambi.txt"], columns="LOC ORG PER MISC ALL".split())
# print(ress_df.to_latex())


def _as_decimal(num: float) -> Decimal:
    # Always round .5 up, not towards even numbers as is the default
    rounder = Context(rounding=ROUND_HALF_UP, prec=4)
    return rounder.create_decimal_from_float(num * 100)


def result2latex(results: "ScoringResult") -> None:
    res = []
    for entity in sorted(results.type_scores):
        scores = results.type_scores[entity]
        counts = results.type_counts[entity]
        res.append([_as_decimal(scores.precision), _as_decimal(scores.recall), _as_decimal(scores.fscore), counts])
    res.append([_as_decimal(results.score.precision), _as_decimal(results.score.recall), _as_decimal(results.score.fscore), results.total_counts])
    res_df = pd.DataFrame(res, index=[entity.types[-1] for entity in results.type_scores] + ["ALL"], columns=["Precision", "Recall", "F1", "Count"])
    return res_df.to_latex()


