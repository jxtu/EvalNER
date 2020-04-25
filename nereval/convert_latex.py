from os.path import join as pjoin
import pandas as pd
from nereval.parse_eval_output import EvalParser


def get_recall(input_file):
    ep = EvalParser(input_file)
    return ep.performance.ALL.recall


output_path = "../data/output"
folder_lst = ["charcnn_wordcnn_crf", "wordlstm_charcnn_crf", "BERT", "stanza", "flair"]
oov_file_lst = ["standard.txt", "oov_token.txt", "oov_full.txt", "oov_type.txt"]
tce_file_lst = ["standard.txt", "tce_ambi.txt", "tce_seen_ambi.txt", "tce_unseen_ambi.txt"]

# recalls = []
#
# for folder in folder_lst:
#     recall_values = [get_recall(pjoin(output_path, pjoin(folder, file))) for file in tce_file_lst]
#     recalls.append(recall_values)
#
# recall_df = pd.DataFrame(recalls, index=folder_lst, columns=tce_file_lst)
# print(recall_df.to_latex())

# all_counts = []
# for file in oov_file_lst + tce_file_lst:
#     ep = EvalParser(pjoin(output_path, pjoin("flair", file)))
#     p = ep.performance
#     counts = [p.LOC.entityCount, p.ORG.entityCount, p.PER.entityCount, p.MISC.entityCount, p.ALL.entityCount]
#     all_counts.append(counts)
#
# all_counts_df = pd.DataFrame(all_counts, index=oov_file_lst+tce_file_lst, columns="LOC ORG PER MISC ALL".split())
# print(all_counts_df.to_latex())
ress = []
for folder in ["flair"]:
    for file in ["standard.txt", "oov_type.txt", "tce_ambi.txt", "tce_seen_ambi.txt", "tce_unseen_ambi.txt"]:
        ep = EvalParser(pjoin(output_path, pjoin(folder, file)))
        p = ep.performance
        res = [p.LOC.recall, p.ORG.recall, p.PER.recall, p.MISC.recall, p.ALL.recall]
        ress.append(res)
ress_df = pd.DataFrame(ress, index=["standard.txt", "oov_type.txt", "tce_ambi.txt", "tce_seen_ambi.txt",
                                    "tce_unseen_ambi.txt"], columns="LOC ORG PER MISC ALL".split())
print(ress_df.to_latex())