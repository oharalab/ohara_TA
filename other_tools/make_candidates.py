import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='filename of 採点者N.txt')

args = parser.parse_args()

data = pd.read_excel(args.filename, encoding="cp932", skiprows=1)
candidates = [i.replace(".0", "") for i in list(set(data[data.columns[0]].astype(str))) if len(i.replace(".0", "")) == 8]
candidates = sorted(candidates)
print(candidates)
with open("../configs/candidates.txt", "w") as f:
    f.write("\n".join(candidates))
