import os
from os import path


def combine_files(folder, out_file):
    in_files = os.listdir(folder)
    with open(out_file, "w") as out_f:
        for i, file in enumerate(in_files):
            lines = open(path.join(folder, file)).readlines()
            out_f.write("-DOCSTART- -X- -X- O\n\n")
            out_f.writelines(lines)
            if (i + 1) % 50 == 0:
                print(i + 1)


if __name__ == "__main__":
    folder_path = "../data/ontonotes_conll/dev"
    out = "../data/ontonotes_conll/ontonotes.dev"
    combine_files(folder_path, out)
