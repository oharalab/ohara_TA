#!/usr/bin/python3
# coding: utf-8
"""
Original author : 平野雅也
Modified by Seiya Ito, 09/30/2018
"""

import argparse
import csv
import collections
import datetime
import glob
import os
import pathlib
import re
import math
import shutil
import subprocess
from subprocess import PIPE
import sys
import time
import traceback
from utils.japanese_converter import zen2han
from utils.reader import *
from utils.score_calculation import *
from utils.tools import *
from utils.writer import *
import zipfile

if sys.version_info[0] != 3:
    raise NotImplementedError('Not supported. Please use Python 3.x')

GCC_BIN = '/usr/bin/gcc'

# 出力ファイル対応
OUTPUT_FILE_NAME = ['out1.txt', 'out2.txt', 'out3.txt', 'out4.txt']

# 無限ループ発生時に書き出すメッセージ内容
INF_MESSAGE = '''プログラムが終了しませんでした
考えられる原因：無限ループ、終了条件の間違い
'''

# 無限ループを判定する猶予
TIMEOUT_SEC = 2


HEADER = '<head>\n'\
         '<meta charset="UTF-8" />\n'\
         '<title>{}</title>\n'\
         '<link rel="stylesheet" href="../html/css/prettify.css" type="text/css">\n'\
         '<link rel="stylesheet" href="../html/css/bootstrap.css" type="text/css">\n'\
         '<link rel="stylesheet" href="../html/css/bootstrap-grid.css" type="text/css">\n'\
         '<link rel="stylesheet" href="../html/css/styles.css" type="text/css">\n'\
         '</head>\n'

FOOTER = '<script src="../html/js/jquery-3.3.1.min.js"></script>\n'\
         '<script src="../html/js/bootstrap.js"></script>\n'\
         '<script src="../html/js/bootstrap.bundle.js"></script>\n'\
         '<script src="../thirdparty/code-prettify/src/prettify.js"></script>\n'\
         '<script src="../thirdparty/code-prettify/loader/lang-css.js"></script>\n'\
         '<script>prettyPrint();</script>\n'

MODAL = '<button type="button" class="btn btn-outline-dark" data-toggle="modal" data-target="#{0}">{0}</button>\n'\
        '<div class="modal fade" id="{0}" tabindex="-1" role="dialog" aria-labelledby="{0}">\n'\
        '<div class="modal-dialog" role="document">\n'\
        '<div class="modal-content">\n'\
        '<div class="modal-body">\n'\
        '{1}\n'\
        '</div>\n'\
        '</div><!-- /.modal-content -->\n'\
        '</div><!-- /.modal-dialog -->\n'\
        '</div><!-- /.modal -->\n'


class Compiler(object):
    """
    """

    def __init__(self, n, input_files=None, output_files=None, stdout_path=None, debug=False):
        """
        :param n: 課題番号
        :param input_files:
        :param output_files:
        :param stdout_path:
        :param debug:
        """
        self.is_pptx = False

        self.ex_num = n

        self.input_files = [] if input_files is None else input_files
        self.output_files = [] if output_files is None else output_files
        self.output_path = stdout_path

        self.debug = debug
        self.nkf = [NKF_BIN, '-w', '--overwrite']
        self.gcc = [GCC_BIN]

    def convert_encoding(self, src):
        """
        ソースコードのエンコードを utf-8 に変換
        :param src: path to source file
        :return:
        """
        ret = True
        try:
            cmd = self.nkf.copy()
            cmd.append(src)
            convert = execute(cmd)
            stdout, stderr = convert.communicate()
        except Exception as e:
            if self.debug:
                print(e)
                traceback.print_exc()
            else:
                pass
            ret = False
        finally:
            pass
        return ret, stderr

    def compile(self, src, out):
        """
        ソースコードをコンパイル
        :param src: ソースコード
        :param out: 実行ファイル名
        :return:
            ret: コンパイルの成功 (True) と失敗 (False)
            error_msg: 標準エラー出力
        """
        ret = True
        cmd = self.gcc.copy()
        cmd.extend(['-o', out, src]) #gcc option:"-std=c11"
        result = execute(cmd)
        _, stderr = result.communicate()
        error_msg = stderr.decode('utf-8')
        if not isinstance(stderr, type(None)):
            if any(t in error_msg for t in ['エラー', 'error']):
                print('Error: Fail to compile {}'.format(src))
                ret = not ret
        return ret, error_msg

    def execute(self, program):
        """
        プログラムを実行し，ファイルに書き出す
        :param program: 実行ファイル
        :return:
            point:csvに出力する点数
        """
        out = {}
        n = max(1, len(self.input_files))
        for i in range(n):
            if out.get(i+1) is None:
                out[i+1] = {}
            out[i+1].update({'point': 0})

            cat_option = None
            with open(self.input_files[i], 'r') as f:
                input_string = f.readlines()
            if len(input_string) != 0 and input_string[-1][:4] == "cat ":
                cat_option = input_string[-1]
                input_string = "".join(input_string[:-1])
            else:
                input_string = "".join(input_string)
            #print(input_string, cat_option)

            if program[-1] in args.cmd_exercise or program[-2] in args.cmd_exercise:
                if not isinstance(input_string, list):
                    cmd = [" ".join(['./' + program, str(input_string).replace("\n", "")])]
                    input_string = ""
                else:
                    cmd = [" ".join(['./' + program, str(input_string[0]).replace("\n", "")])]
                    input_string.pop(0)
            else:
                cmd = ['./' + program]
            #print(subprocess.run(cmd).stdout)
            result = execute(cmd, desc='Exercise: %d Trial: %d' % (self.ex_num, i+1), shell=True)

            if len(self.input_files) > 0:
                input_string = input_string.encode()
                output, error = result.communicate(input_string, timeout=TIMEOUT_SEC)
            else:
                output, error = result.communicate(timeout=TIMEOUT_SEC)
            #print(output, error)

            # 無限ループ対策
            if result.wait(TIMEOUT_SEC) is None:
                result.kill()
                # プロセス解放待ち
                time.sleep(1)
                out[i+1].update({'std': INF_MESSAGE})
                out[i+1].update({'point': 3})
            else:
                if result.returncode != 0:
                    # 故意に return 1 を返すこともあるため，output があればエラーとしない
                    if len(output) != 0:
                        error = b''
                    elif result.returncode == -11:
                        error = b'segmentation fault\n'
                    else:
                        error = b'return code %d\n' % result.returncode

                cat_result = ""
                if cat_option is not None:
                    cat_result += "\n"
                    cat_result += subprocess.run(cat_option.split(), stdout = PIPE, stderr = PIPE).stdout.decode('utf-8', errors="ignore")
                out[i+1].update({'std': output.decode('utf-8', errors="ignore")+cat_result, 'stderr': error.decode('utf-8')})

                if cat_option is not None:
                    # cat 対象のファイルは一度消す（そうでないと，同じ結果が採点に使われるため）
                    subprocess.call(["rm", cat_option.split()[-1]])

                out[i + 1].update({'point': 4})
                if self.output_path is not None:
                    out[i+1].update({
                        'file': self.write_output(i)
                    })
                out[i + 1].update({'point': 5})

        try:
            files = glob.glob(str(program) + '*')
            for f in files:
                os.remove(f)
        except Exception as e:
            if self.debug:
                print(e)
                traceback.print_exc()
        finally:
            pass

        return out

    def write_output(self, idx):
        """
        出力ファイルの内容をファイルに書き出す
        :return:
        """
        try:
            with open(os.path.join(self.output_path, os.path.basename(self.input_files[idx])), 'r') as output_file:
                return output_file.readlines()
        except Exception as e:
            if self.debug:
                print(e)
                print('Fail to read output file: %s' % OUTPUT_FILE_NAME[self.ex_num])
            return None

def zip2dict(zip_filename, students):
    # 正確には zip ではないが，Friday 側との互換性のため変数名は zipfiles
    zipfiles = {}
    folder_list = sorted(glob.glob(zip_filename+"/*"))
    folder_list = [folder for folder in folder_list if folder[-2] == "_"] + [folder for folder in folder_list if folder[-2] == "1"]
    #print(folder_list)
    for exercise in folder_list:
        if "ex"+str(args.exercise) not in os.path.basename(exercise) or \
            (os.path.basename(exercise)[-1] not in args.use_exercise and \
            os.path.basename(exercise)[-2:] not in args.use_exercise):
            continue
        print("採点対象； {0}".format(exercise))

        for name_file in sorted(glob.glob(exercise+"/*")):
            student_id = os.path.basename(name_file)
            #print(student_id)
            assert student_id in students, "履修者名簿にない学籍番号です．チェックしてください．"
            program_file, submit_id = "", 0
            for p_file in sorted(glob.glob(exercise+"/"+student_id+"/*")):
                try:
                    m = re.search('([0-9]{8})_a[0-9]{7}_([0-9]{2})', os.path.basename(p_file))
                    temp_id = int(m.group(2))
                except:
                    temp_id = 1
                if temp_id > submit_id:
                    submit_id = temp_id
                    program_file = p_file

            #print(student_id, submit_id)
            if student_id not in zipfiles:
                zipfiles[student_id] = [(submit_id, program_file)]
            else:
                zipfiles[student_id].append((submit_id, program_file))

    return zipfiles


def main(args=None):
    """
    :param args:
    :return:
    """
    students = get_students(args.students)
    exercise_path = args.exercise_path % args.exercise
    answers_path = os.path.join(exercise_path, 'answers')
    temp_path = os.path.join(exercise_path, 'temps')
    exercise_sentences_path = os.path.join(exercise_path, 'sentences')
    unzip_sentences_files(exercise_sentences_path)
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
        elif os.path.exists(os.path.join(temp_path, 'ex%d' % (i+1))):
            temp_paths = [os.path.join(os.path.join(temp_path, 'ex%d' % (i+1)), trial) \
                            for trial in sorted(os.listdir(os.path.join(temp_path, 'ex%d' % (i+1))))]

            answers[i] =  {j+1: \
                                {'point': 0, \
                                'std': read_html_answer(path), \
                                'stderr': ''} \
                                for j, path in enumerate(temp_paths)}
        else:
            answers[i] = {}
    print("answers", answers)


    # 辞書初期化
    scoring = collections.OrderedDict()

    # 正確には zipfile ではなく，構造を展開して dict 化したもの
    zipfiles = zip2dict(args.zip, students)
    #print(zipfiles)

    student_ids = sorted(zipfiles.keys())
    for student_id, zfiles in zipfiles.items():
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
        for submit_id, program_file in zfiles:
            #print(submit_id, program_file)
            try:
                name = os.path.basename(program_file)
                ex_num, name_check = detect_exercise_num(name)
                print(ex_num)
                if ex_num == -1:# or ex_num >= len(compilers):
                    continue

                # cp to tmp directory
                file_path = os.path.join(extract_dir, name)
                shutil.copyfile(program_file, file_path)

                # 辞書に書きこんでおく
                program_info = dict()
                program_info['task'] = ex_num
                program_info['file_path'] = file_path
                # get timestamp
                program_info['timestamp'] =  datetime.datetime.fromtimestamp(pathlib.Path(program_file).stat().st_ctime)
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
                        out_file.write('<!-- class="code length" code length '+ str(0) +" -->")
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
                    if str(i+1) not in args.fixed_exercise:
                        compiled_name = student_id + "_ex" + str(i+1)
                    else:
                        compiled_name = "ex" + str(args.exercise) + "_" + str(i+1)

                    ret, msg = compiler.compile(program_info['file_path'], compiled_name)
                    if not ret:
                        saiten['ex%d' % (i + 1)] = 2
                        program_info['status'] = 'NG (Compile Error)'
                    else:
                        # 対象プログラムを実行
                        results = compiler.execute(compiled_name)
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
    parser.add_argument('-c', '--csv', help='make csv', default=True)
    parser.add_argument('--cmd_exercise', help='exercie num that need to use command line arguments (e.g. 1+2+3)', default="", type=str)
    parser.add_argument('-d', '--debug', help='debug mode', default=False, type=bool)
    parser.add_argument('-e', '--exercise', help='the number of exersice', default=4, type=int)
    parser.add_argument('--exercise_path', help='the directory of exercise', default='./exercise/ex%d')
    parser.add_argument('--execution_dir', help='the directory of execution (test) environment', default='./execution_dir')
    parser.add_argument('--fixed_exercise', help='the number of exercise which name is fixed', default="", type=str)
    parser.add_argument('--input_dir', help='input files in this dir that is needed to execute program properly',
                        default='./configs/inputs')
    parser.add_argument('-n', '--num_tasks', help='number of tasks', default=4, type=int)
    parser.add_argument('-o', '--output_dir', help='output directory', default='./output')
    parser.add_argument('-s', '--students', help='the path of student file', default='./configs/students.txt')
    parser.add_argument('-t', '--tmp', help='path to tmp', default='./tmp')
    parser.add_argument('-u', '--use_exercise', help='use exercie num (e.g. 1+2+3)', default=None, type=str)
    parser.add_argument('-z', '--zip', help='path to zip', default='./zip')

    args = parser.parse_args()
    if args.use_exercise is None:
        args.use_exercise = [str(i) for i in range(1, args.num_tasks+1)]
    else:
        args.use_exercise = args.use_exercise.split("+")
    print(args.use_exercise)

    args.cmd_exercise = set(args.cmd_exercise.split("+"))
    args.fixed_exercise = set(args.fixed_exercise.split("+"))

    for filename in os.listdir(args.input_dir):
        print(filename)
        subprocess.call(["rm", filename])
        subprocess.call(["cp", os.path.join(args.input_dir, filename), filename])
        subprocess.call(["chmod", "444", filename])

    subprocess.call(["rm", "-r", args.tmp])
    os.makedirs(args.tmp)

    subprocess.call(["rm", "-r", args.output_dir])
    os.makedirs(args.output_dir)

    main(args)


    if args.csv:
        subprocess.call(["python3", "other_tools/make_csv.py", "-n", str(args.num_tasks)])
