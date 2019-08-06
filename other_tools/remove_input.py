import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', help='path to dir', default='')
    parser.add_argument('-p', '--pass_sentence', help='pass sentence num', default=0, type=int)
    parser.add_argument('-r', '--remove_phrase', help='remove_phrase', default=None)
    args = parser.parse_args()

    for path in os.listdir(args.dir):
        with open(os.path.join(args.dir, path), "r") as f:
            data = f.readlines()
        with open(os.path.join(args.dir, path), "w") as f:
            if args.remove_phrase is not None:
                f.write("".join([line.replace(args.remove_phrase, "") for line in data[args.pass_sentence:]]))
            else:
                f.write("".join(data[args.pass_sentence:]))
