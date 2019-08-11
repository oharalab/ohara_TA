# a や　b の入ったディレクトリの簡易的な修正
# python revise_file.py -z 'temp/ex9' 

import argparse
import glob
import os
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-z', '--zipfile', help='zipfile or directory')
parser.add_argument('-c', '--character', default = "b", help='character should be replace or remove')
args = parser.parse_args()

for directory in os.listdir(args.zipfile):
    """
    # このやり方では，ファイルが存在しない場合に厳しい
    candidates = os.listdir(os.path.join(args.zipfile, directory))
    word_document = [document for document in candidates if ".doc" in document]
    if len(word_document) == len(candidates) and len(candidates) != 0:
        print(directory, True)
    """
    
    if directory[-1] == "a":
        subprocess.run(["rm", "-r", os.path.join(args.zipfile, directory)])
    elif directory[-1] == args.character:
        candidates = glob.glob(os.path.join(args.zipfile, directory))
        for cand in candidates:
            for st_id in glob.glob(os.path.join(cand, "*")):
                for filename in glob.glob(os.path.join(st_id, "*")):
                    #print(filename)
                    if filename[-3:] in {args.character+".c", args.character+".cpp"}:
                        subprocess.run(["mv", filename, filename.replace(args.character+".c", ".c")])
        target = directory.replace(args.character, "")
        subprocess.run(["mv", os.path.join(args.zipfile, directory),
                        os.path.join(args.zipfile, target)])
        
