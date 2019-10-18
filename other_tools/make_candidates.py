with open("students.txt", "r") as fr:
    candidates = [line.split()[0] for line in fr]
    print(candidates)
    with open("candidates.txt", "w") as fw:
        fw.write("\n".join(candidates))
"""
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='filename of 採点者-N.txt')

args = parser.parse_args()

data = pd.read_excel(args.filename, encoding="cp932", skiprows=1)
candidates = [i.replace(".0", "") for i in list(set(data[data.columns[0]].astype(str))) if len(i.replace(".0", "")) == 8]
candidates = sorted(candidates)
print(candidates)
with open("../configs/candidates.txt", "w") as f:
    f.write("\n".join(candidates))
"""
