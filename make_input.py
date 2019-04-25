import argparse
from bs4 import BeautifulSoup
import difflib
import numpy as np
import os
import shutil
import zipfile

def make_directory(target_paths):
    for target_path in target_paths:
        if not os.path.exists(target_path):
            os.makedirs(target_path)

def make_sentences(origin_path, unzip_path, sentence_path):
    sentence_path = sentence_path + "/"
    shutil.copyfile(origin_path, unzip_path + ".zip")
    with zipfile.ZipFile(origin_path) as zfile:
        zfile.extractall(path=sentence_path)

def make_trials(filename, contents):
    with open(filename, "w", encoding="utf8") as f:
        f.write(contents)

def read_html_answer(filename, encoding='utf8'):
    with open(filename, 'rb') as f:
        html_data = f.read()
    soup = BeautifulSoup(html_data, "lxml")
    result = search_answers(str(soup))
    return result

def search_answers(text):
    target = "実行結果例"
    end_sentence = "<p>　</p>\n<p>　</p>\n<p>　</p>"
    text = text.split(end_sentence)[0]
    #text = text.replace("<br />", "<br/>").replace("<br>", "<br/>")
    values = [text for text in text.split("\n")]#for small_text in text.split("<p>")]

    indexes = []
    for i, line in enumerate(values):
        line = str(line)
        if "以下の" in line or "ように" in line or "ような" in line:
            continue

        for j in range(len(line)):
            score = difflib.SequenceMatcher(None, target, line[j:j+5]).ratio()
            if score >= 0.5:
                indexes.append(i)
                break
    indexes.append(len(values))

    answers = []
    for i in range(len(indexes) - 1):
        text = "<html>"+"".join(values[indexes[i]+1:indexes[i+1]])+"</html>"
        answers.append(BeautifulSoup(text, "lxml"))

    result = []
    for answer in answers:
        text = []
        check = False
        remove_ans = [[str(font) for font in sub.findAll("font")] for sub in answer if len(sub.findAll("font")) != 0]
        answer_text = str(answer)
        for remove_array in remove_ans:
            for remove in remove_array:
                 answer_text = answer_text.replace(remove, "INPUT_STRING")
        answer_text = BeautifulSoup(answer_text, "lxml")

        #for line in answer.text.split("\r"):
        prev_line = "dammy sentence"
        for line in answer_text.text.split("\r"):
            line = line.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("‾", "~")
            if line == prev_line:
                break
            prev_line = str(line)
            if not check:
                if line not in [" ", "", "\r"]:
                    check = True
                    text.append(line)
            else:
                text.append(line)

        result.append(["\n".join(text).replace("INPUT_STRING\n", "").replace("INPUT_STRING", ""),
                       "\n".join([inp.text for inp in
                                  answer.findAll("font")])])

    return result

def delete_interupt(text, length):
    text = text.split("\n")[:length-1]
    return "\n".join(text)


def make_answers(unzip_path, input_path, temp_path):
    html_paths = [filename
                  for filename in os.listdir(unzip_path)
                  if "ex" in filename]
    input_paths = [input_path + "/ex" + str(i) for i in range(1, 1+len(html_paths))]
    temp_paths = [temp_path + "/ex" + str(i) for i in range(1, 1 + len(html_paths))]
    html_paths = [unzip_path + "/" + html_path for html_path in html_paths if html_path[-3:] != "txt"]

    make_directory(input_paths)
    make_directory(temp_paths)
    answers_dict = {}
    for html_path in html_paths:
        answers_dict[html_path] = read_html_answer(html_path)

    for i, key in enumerate(sorted(answers_dict.keys())):
        answers = answers_dict[key]
        print("task", i)
        for j, answer in enumerate(answers):
            print("trial", j)
            if answer[1].split("\n")[-1] == "^Z":
                answer[0]= delete_interupt(answer[0], len(answer[1].split("\n")))
                answer[1]= delete_interupt(answer[1], len(answer[1].split("\n")))
                print(answer[0])
                print(answer[1])
                make_trials(temp_paths[i] + "/trial" + str(j+1) + ".txt", answer[0])
                make_trials(input_paths[i] + "/trial" + str(j+1) + ".txt", answer[1])
            else:
                print(answer[0])
                print(answer[1])
                make_trials(temp_paths[i] + "/trial" + str(j+1) + ".txt", answer[0])
                make_trials(input_paths[i] + "/trial" + str(j+1) + ".txt", answer[1])
            print()

def make_contents(origin_path, target_path):
    target_dir = "exercise/"
    unzip_path = target_path
    target_path = target_dir+target_path[:-2]
    input_path = target_path + "/inputs"
    sentence_path = target_path + "/sentences"
    temp_path = target_path + "/temps"
    unzip_path = sentence_path + "/" + unzip_path
    make_directory([target_path, input_path, sentence_path, temp_path])
    make_sentences(origin_path, unzip_path, sentence_path)
    make_answers(unzip_path, input_path, temp_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--zip', help='path to zip', default='./test/ex5th.zip')

    args = parser.parse_args()

    target_path = args.zip.split("/")[-1].replace(".zip", "")

    make_contents(args.zip, target_path)
