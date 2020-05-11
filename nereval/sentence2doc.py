import argparse


def sentence2doc(conll_file, out_file):
    doc_start = "-DOCSTART- O"
    with open(out_file, "w") as wf:
        with open(conll_file, 'r') as f:
            wf.write(doc_start + "\n\n")
            for line in f:
                if line == "\n":
                    wf.write(line + doc_start + line * 2)
                else:
                    wf.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("conll_file")
    parser.add_argument("out_file")

    args = parser.parse_args()
    sentence2doc(args.conll_file, args.out_file)