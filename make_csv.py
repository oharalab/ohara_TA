import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--max_score', default=1.0,
                    help='the score is needed to get the max score 5. The desirable value is 1; however some wrong cases happen.')
parser.add_argument('-s', '--score_rate', default=0.3,
                    help='the score is needed to get 4 score by rate * max_score')
parser.add_argument('-l', '--code_length_rate', default=0.5,
                    help='the score is needed to get 2 score by rate * code_length that the almost correct code has')

args = parser.parse_args()


target_htmls = ["output/"+html for html in sorted(os.listdir("output"))]

score_dict = dict()
for target in target_htmls:
    with open(target, "r") as f:
        student_id = target.replace("output/out_", "")[:-5]
        #print(student_id)
        code_length = []
        scores = []
        for line in f:
            code_def = '<!-- class="code length" code length '
            score_def = '<!-- class="averagescore" average score '
            if "Exercise" in line:
                #print(line)
                pass
            if code_def in line:
                line = line.split(code_def)[1]
                line = line.split(" -->")[0]
                line = int(line)
                #print(line)
                code_length.append(line)
            elif score_def in line:
                line = line.split(score_def)[1]
                line = line.split(" -->")[0]
                line = float(line)
                #print(line)
                scores.append(line)
        code_length = [code_length[i] if i < len(code_length) else 0 for i in range(4)]
        scores = [scores[i] if i < len(scores) else 0 for i in range(4)]
        score_dict[student_id] = [code_length, scores]

#print(score_dict)

code_info = [0.000001] * 8 # task1 ~ task4 (average code len, num)
score_info = [0.000001] * 8

for value in score_dict.values():
    code_len = value[0]
    scores = value[1]
    for i,score in enumerate(scores):
        if score != 0: # nedd to modity
            code_info[i*2] += code_len[i]
            code_info[i*2+1] += 1
            score_info[i*2] += score
            score_info[i*2+1] += 1

task_code = []
task_score = []
for i in range(4):
    task_code.append(code_info[i*2]/code_info[i*2+1])
    task_score.append(score_info[i*2]/score_info[i*2+1])
task_score = [score if score >= 0.1 else 0.1 for score in task_score]
print(task_code)
print(task_score)

code_len_rate = float(args.code_length_rate)
score_rate = float(args.score_rate)
max_score = float(args.max_score)


with open("easy_score.csv", "w") as f:
    for key, value in score_dict.items():
        info = []
        code_len = value[0]
        scores = value[1]
        easy_scores = [0] * 4
        for i,score in enumerate(scores):
            if score >= max_score:
                #print(score, 5)
                easy_scores[i] = "5"
            elif score >= task_score[i] * score_rate:
                #print(score, 4)
                easy_scores[i] = "4"
            elif score != 0:
                #print(score, 3)
                easy_scores[i] = "3"
            elif code_len[i] == 0:
                #print(score, code_len, 0)
                easy_scores[i] = "0"
            elif code_len[i] >= task_code[i] * code_len_rate:
                #print(score, code_len, 2)
                easy_scores[i] = "2"
            else:
                #print(score, code_len, 1)
                easy_scores[i] = "1"
        info.append(key)
        info.extend(easy_scores)
        f.write(",".join(info) + "\n")

with open("easy_subscore.csv", "w") as f:
    for key, value in score_dict.items():
        info = []
        code_len = value[0]
        scores = value[1]
        easy_scores = [0] * 4
        for i,score in enumerate(scores):
            if score >= max_score:
                #print(score, 5)
                easy_scores[i] = "5"
            elif score != 0:
                #print(score, 3)
                easy_scores[i] = "3"
            elif code_len[i] == 0:
                #print(score, code_len, 0)
                easy_scores[i] = "0"
            else:
                #print(score, code_len, 1)
                easy_scores[i] = "1"
        info.append(key)
        info.extend(easy_scores)
        f.write(",".join(info) + "\n")
