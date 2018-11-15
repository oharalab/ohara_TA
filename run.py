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


def main(args=None):
    """

    :param args:
    :return:
    """
    students = {}
    with open(args.students) as f:
        for line in f.readlines():
            s, n = line.strip().split(' ')
            students[s] = n

    exercise_path = args.exercise_path % args.exercise
    answers_path = os.path.join(exercise_path, 'answers')
    exercise_sentences_path = os.path.join(exercise_path, 'sentences')

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

        prev, program_info = None, None
        with open(os.path.join(args.output_dir, '{}_{}.html'.format('out', student_id)), 'w') as out_file:
            out_file.write(
                '<!DOCTYPE html>\n'
                '<html lang="ja">\n'
            )

            out_file.write(HEADER.format(student_id))
            out_file.write('<body>\n')
            out_file.write('<header class="navbar navbar-expand navbar-dark flex-column flex-md-row bd-navbar">'
                           '</header>')
            out_file.write('<div class="container">\n')
            out_file.write('<div class="row">\n')
            out_file.write('<div class="col-md-2">\n')
            out_file.write('<div class="sidebar content-box">\n')
            out_file.write('<ul class="nav">\n')
            for sid in student_ids:
                out_file.write('<li class="{1}">'
                               '<a href="out_{0}.html">{0}</a>'
                               '</li>\n'.format(sid, 'current' if sid == student_id else ''))
            out_file.write('</ul>\n')
            out_file.write('</div>\n')
            out_file.write('</div>\n')
            out_file.write('<div class="col-md-10">\n')
            out_file.write('<div class="row">\n')
            out_file.write('<div class="col-md-8">\n')
            out_file.write('<h3>{} {}</h3>\n'.format(student_id, students[student_id]))
            out_file.write('</div><!-- col-md-8 -->\n')
            out_file.write('<div class="col-md-4">\n')
            for path in sorted(glob.glob(os.path.join(exercise_sentences_path, '**'), recursive=True)):
                if re.match('ex[0-9]+_[0-9]+.html', os.path.basename(path)):
                    name = os.path.splitext(os.path.basename(path))[0]
                    out_file.write(MODAL.format(name, read_html_body(path)))
            out_file.write('</div><!-- col-md-4 -->\n')
            out_file.write('</div><!-- row -->\n')

            # tab
            out_file.write('<ul class="nav nav-tabs">\n')
            for i in range(len(compilers)):
                out_file.write(
                    '<li class="nav-item">\n'
                    '<a href="#ex{0}" class="nav-link {1}" data-toggle="tab">Exercise {0}</a>\n'
                    '</li>\n'.format(i+1, '' if i > 0 else 'active')
                )
            out_file.write('</ul>\n')
            out_file.write('<div class="tab-content">\n')
            for i, compiler in enumerate(compilers):
                ret = False
                results = {}

                if i > 0:
                    out_file.write('</div>  <!-- tab{}-->\n'.format(i))
                out_file.write('<div id="ex{}" class="tab-pane {}">\n'.format(i+1, '' if i > 0 else 'active'))
                try:
                    if verify.get(i) is None:
                        write_not_submitted(out_file)
                        continue
                    if i > 0:
                        prev = program_info
                    program_info = get_latest_program_info(verify[i])

                    # 時間の判定
                    if prev is not None:
                        if prev['timestamp'] < program_info['timestamp']:
                            program_info['timestamp_status'] = 'OK'
                        else:
                            program_info['timestamp_status'] = 'NG'
                    else:
                        program_info['timestamp_status'] = 'OK'

                    # コードの内容をファイルに書き出す
                    ret, msg = compiler.convert_encoding(program_info['file_path'])
                    if not ret:
                        print('Cannot convert encoding')

                    # 対象ソースコードをコンパイル
                    ret, msg = compiler.compile(program_info['file_path'], student_id)
                    if not ret:
                        saiten['ex%d' % (i + 1)] = 2
                        program_info['status'] = 'NG (Compile Error)'
                    else:
                        # 対象プログラムを実行
                        results = compiler.execute(student_id)
                        saiten['ex%d' % (i + 1)] = 5
                        program_info['status'] = 'OK' if program_info['name_check'] else 'NG (Naming rule)'
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    program_info['status'] = 'NG (Naming rule)'
                finally:
                    pass

                write_program_info(program_info, out_file)
                write_code(program_info['file_path'], out_file)
                if ret:
                    write_trials(results, answers, i, out_file)
                else:
                    write_error_msg(msg, out_file)

            scoring[student_id] = saiten
            out_file.write('</div>\n')
            out_file.write('</div> <!-- div.tab-content -->\n')
            out_file.write('</div> <!-- div.col-md-10 -->\n')
            out_file.write('</div> <!-- div.row -->\n')
            out_file.write('</div> <!-- div.container -->\n')

            out_file.write(FOOTER)
            out_file.write('</body>')
            out_file.write('</html>')

    print('Complete!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-z', '--zip', help='path to zip', default='./zip')
    parser.add_argument('-t', '--tmp', help='path to tmp', default='./tmp')
    parser.add_argument('-n', '--num_tasks', help='number of tasks', default=4, type=int)
    parser.add_argument('-d', '--debug', help='debug mode', default=False, type=bool)
    parser.add_argument('-o', '--output_dir', help='output directory', default='./output')
    parser.add_argument('-e', '--exercise', help='', default=4, type=int)
    parser.add_argument('--exercise_path', help='', default='./exercise/ex%d')
    parser.add_argument('-s', '--students', help='', default='./students.txt')

    args = parser.parse_args()

    if not os.path.exists(args.tmp):
        os.makedirs(args.tmp)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    main(args)
