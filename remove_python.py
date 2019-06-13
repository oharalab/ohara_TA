import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='path to dir', default='')
    parser.add_argument('-p', '--pass_sentence', help='pass sentence num', default=1, type=int)
    args = parser.parse_args()

    for path in os.listdir(args.dir):
        with open(os.path.join(args.dir, path), "r") as f:
            data = f.readlines()
        with open(os.path.join(args.dir, path), "w") as f:
            f.write("\n".join(data[args.pass_sentence:]))
