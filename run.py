#!/usr/bin/python3
# coding: utf-8
"""
author : 平野雅也
"""

import argparse
import collections
import datetime
import glob
import os
import re
import shutil
import sys
import traceback
import zipfile

from autocompiler import Compiler
from autocompiler import Makehtml

def read_student_list(student_list):
    '''students.txtの読み込み'''
    students = {}
    with open(student_list) as f:
        for line in f.readlines():
            s, n = line.strip().split(' ')
            students[s] = n
    return students

def detect_exercise_num(file_path, offset=-1):
    """
    課題番号を検出
    :param file_path: 展開したファイルのパス
    :param offset:
    :return: 課題番号. 課題番号がない場合は-1.
    """

    filename = os.path.split(file_path)[1]
    if not filename:
        return -1, None

    match_obj = re.search('(ex)?[0-9]{1,2}_([0-9])\.(\w+)$', filename)
    if isinstance(match_obj, type(None)):
        return -1, None

    ex_check = match_obj.group(1) == 'ex'
    basename = match_obj.group(2)
    ext = match_obj.group(3)
    if not file_path.startswith('_'):
        if re.match(ext, 'c(pp)?') is not None or ext == 'pptx':
            if not ex_check:
                print('Warning: File does not starts with "ex". {}'.format(filename))
            exercise_num = int(basename)
            return exercise_num + offset, ex_check
        else:
            return -1, ex_check


def get_latest_program_info(program_info):
    valid = False
    name_checks = [program_info[i]['name_check'] for i in range(len(program_info))]
    timestamps = [program_info[i]['timestamp'] for i in range(len(program_info))]

    idx = 0
    for i, (n, t) in enumerate(zip(name_checks, timestamps)):
        if valid and not n:
            continue
        elif not valid and n:
            valid = n
            idx = i
        else:
            if timestamps[idx] < timestamps[i]:
                idx = n

    return program_info[idx]



def main(args=None):
    if sys.platform == 'cygwin':
        NKF_BIN = './bin/nkf32.exe'
    else:
        NKF_BIN = 'nkf'
    """

    :param args:
    :return:
    """

    students = read_student_list(args.students)

    #ディレクトリexercise/ex%dの設定
    exercise_path = args.exercise_path % args.exercise
    #ディレクトリexercise/ex%d/answersの設定
    answers_path = os.path.join(exercise_path, 'answers')
    #ディレクトリexercise/ex%d/sentencesの設定
    exercise_sentences_path = os.path.join(exercise_path, 'sentences')
    #zipファイルが有るか確認、なければエラー
    exercise_sentences_files = glob.glob(os.path.join(exercise_sentences_path, '*'))
    if len(exercise_sentences_files) == 1:
        filename = exercise_sentences_files[0]
        if os.path.splitext(filename)[1] == '.zip':
            with zipfile.ZipFile(filename) as zfile:
                zfile.extractall(path=exercise_sentences_path)
    elif len(exercise_sentences_files) < 1:
        raise FileNotFoundError('No files in exercise path')
    else:
        pass

    input_files_path = os.path.join(exercise_path, 'inputs')
    output_files_path = os.path.join(exercise_path, 'outputs')

    compilers, answers = [], {}
    for i in range(args.num_tasks):
        input_files = sorted(glob.glob(os.path.join(input_files_path, 'ex%d' % (i+1), '*')))
        output_files = sorted(glob.glob(os.path.join(output_files_path, 'ex%d' % (i+1), '*')))

        if len(input_files) != len(output_files):
            compilers.append(Compiler(i, input_files=input_files, output_files=None))
        elif len(input_files) == len(output_files):
            compilers.append(Compiler(i, input_files=input_files, output_files=output_files))
        else:
            compilers.append(Compiler(i))

        if os.path.exists(os.path.join(answers_path, 'ex%d' % (i+1))):
            program_name = 'answer'
            src = glob.glob(os.path.join(answers_path, 'ex%d' % (i+1), '*.c'))[0]
            compilers[i].convert_encoding(src)
            compilers[i].compile(src, program_name)
            answers[i] = compilers[i].execute(program_name)
        else:
            answers[i] = {}

    # 辞書初期化
    scoring = collections.OrderedDict()

    zipfiles = {}
    for zfile in sorted(glob.glob(os.path.join(args.zip, '*.zip'))):
        m = re.search('([0-9]{8})_a[0-9]{7}_([0-9]{2})', os.path.basename(zfile))
        student_id = m.group(1)
        submit_id = int(m.group(2))

        if zipfiles.get(student_id) is None:
            zipfiles[student_id] = (submit_id, zfile)
        else:
            if zipfiles[student_id][0] < submit_id:
                zipfiles[student_id] = (submit_id, zfile)

    student_ids = sorted(zipfiles.keys())

    for student_id, (_, zfile) in zipfiles.items():
        saiten = {}
        for i in range(args.num_tasks):
            saiten.update({'ex%d' % (i + 1): 0})

        saiten['s_id'] = student_id
        verify = {}
        extract_dir = os.path.join(args.tmp, student_id)

        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        # zip内のファイルを1つずつ参照
        # timestampの対策のため、コードを分割する
        with zipfile.ZipFile(zfile) as data:
            for name in data.namelist():
                try:
                    ex_num, name_check = detect_exercise_num(name)

                    if ex_num == -1 or ex_num >= len(compilers):
                        continue

                    data.extract(name, path=extract_dir)

                    # get timestamp
                    info = data.getinfo(name)
                    d = info.date_time

                    # 辞書に書きこんでおく
                    program_info = dict()
                    program_info['task'] = ex_num
                    program_info['file_path'] = os.path.join(extract_dir, name)
                    program_info['timestamp'] = datetime.datetime(d[0], d[1], d[2], d[3], d[4], d[5])
                    program_info['name_check'] = name_check
                    if verify.get(ex_num) is None:
                        verify[ex_num] = []
                    verify[ex_num].append(program_info)

                    # pptx なら展開
                    if compilers[ex_num].is_pptx:
                        shutil.copy2(os.path.join(extract_dir, name), os.path.join(args.output_dir, student_id + name))
                        continue
                except KeyboardInterrupt:
                    print('強制終了します')
                    sys.exit(0)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    print('原因不明')

        Makehtml.create_html(args.output_dir, student_id)

    print('Complete!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--zip', help='path to zip', default='./zip')
    parser.add_argument('-t', '--tmp', help='path to tmp', default='./tmp')
    parser.add_argument('-n', '--num_tasks', help='number of tasks', default=4, type=int)
    parser.add_argument('-d', '--debug', help='debug mode', default=False, type=bool)
    parser.add_argument('-o', '--output_dir', help='output directory', default='./output')
    parser.add_argument('-e', '--exercise', help='number of excrcises', type=int)
    parser.add_argument('--exercise_path', help='', default='./exercise/ex%d')
    parser.add_argument('-s', '--students', help='', default='./students.txt')
    parser.add_argument('-l', '--timeout', help='', default=1, type=int)
    parser.add_argument('-gcc','--gcc_path', help='path to gcc', default='/usr/bin/gcc')

    args = parser.parse_args()

    if not os.path.exists(args.tmp):
        os.makedirs(args.tmp)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    main(args)
