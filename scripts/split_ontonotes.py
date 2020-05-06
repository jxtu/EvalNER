import os
from os import path


def select_by_ids(id_file: str, data_dir: str, mode: str):
    file_paths = open(id_file)
    for file_path in file_paths:
        dirs = file_path.strip().split("/")
        file_name = dirs[-1] + ".conll"
        sub_folder = dirs[3]
        os.system(
            f"cp {path.join(data_dir, sub_folder, file_name)} {path.join(data_dir, mode)}"
        )


if __name__ == "__main__":
    id_file = "../data/ontonotes_conll/english-ontonotes-5.0-conll-2012-test-document-ids.txt"
    data_dir = "../data/ontonotes_conll"
    mode = "test_conll2012"
    select_by_ids(id_file, data_dir, mode)

