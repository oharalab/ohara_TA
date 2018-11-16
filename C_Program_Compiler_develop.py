#!/usr/bin/python3
# coding: utf-8
"""
Original author : 平野雅也

Modified by Seiya Ito, 09/30/2018
"""

import csv
import collections
import datetime
import glob
import os
import re
import shutil
import subprocess
from subprocess import PIPE
import sys
import time
import traceback
import zipfile
import argparse

if sys.version_info[0] != 3:
    raise NotImplementedError('Not supported. Please use Python 3.x')

if sys.platform == 'cygwin':
	NKF_BIN = './bin/nkf32.exe'
else:
	NKF_BIN = 'nkf'

GCC_BIN = '/usr/bin/gcc'

# 出力ファイル対応
OUTPUT_FILE_NAME = ['out1.txt', 'out2.txt', 'out3.txt', 'out4.txt']

# 無限ループ発生時に書き出すメッセージ内容
INF_MESSAGE = '''プログラムが終了しませんでした
考えられる原因：無限ループ、終了条件の間違い
'''

# 無限ループを判定する猶予
TIMEOUT_SEC = 1


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


MODAL =  '{1}\n'



def execute(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False, desc=''):
    """

    :param args:
    :param stdout:
    :param stdin:
    :param stderr:
    :param shell:
    :param desc:
    :return:
    """
    if desc != '':
        desc += '\t'
        print(desc + ' '.join(args))
    return subprocess.Popen(args, stdout=stdout, stdin=stdin, stderr=stderr, shell=shell)


def read_html_body(filename, encoding='shift-jis'):
    with open(filename, 'rb') as f:
        html_data = f.read().decode(encoding)
    _, html_data = html_data.split('<body')
    idx = html_data.find('>') + 1
    html_data, _ = html_data[idx:].split('</body')
    return html_data


def write_summary(timestamp, timestamp_status, file_path, status, out_file):
    contents = '<table class="table table-bordered">\n' \
               '<thead>\n' \
               '<tr>\n' \
               '<th></th>\n' \
               '<th>Content</th>\n' \
               '<th>Status</th>\n' \
               '</tr>\n' \
               '</thead>\n' \
               '<tbody>\n' \
               '<tr>\n' \
               '<th>Timestamp</th>\n' \
               '<td>{}</td>\n' \
               '<td>{}</td>\n' \
               '</tr>\n' \
               '<tr>' \
               '<th>Code</th>\n' \
               '<td>{}</td>\n' \
               '<td>{}</td>\n' \
               '</tr>\n' \
               '</tbody>\n' \
               '</table>\n'

    out_file.write(contents.format(
        timestamp,
        timestamp_status,
        file_path,
        status
    ))


def write_not_submitted(out_file):
    write_summary('None', 'NG', 'Not found', 'NG', out_file)


def write_program_info(program_info, out_file):
    write_summary(
        program_info['timestamp'].strftime("%c"),
        program_info['timestamp_status'],
        program_info['file_path'],
        program_info['status'],
        out_file)


def write_code(src, out_file):
    """
    コードの内容をファイルに書き出す
    :param src: path to source file
    :param out_file: 書き込みファイル
    :return:
    """

    escape_seq = {
        '&': '&amp;',
        '<':  '&lt;',
        '>': '&gt;',
    }

    out_file.write('<pre class="prettyprint linenums">\n')

    ret = False

    try:
        convert = execute([NKF_BIN, '-w', '--overwrite', src])
        stdout, stderr = convert.communicate()
        with open(src, 'r') as f:
            for line in f.readlines():
                for k, v in escape_seq.items():
                    line = line.replace(k, v)
                out_file.write(line)
    except Exception as e:
        print(e)
        traceback.print_exc()

    out_file.write('</pre>\n')

    return ret


def write_trials(results, answers, task, out_file):
    """

    :param results: path to source file
    :param answers: path to source file
    :param task:
    :param out_file: 書き込みファイル
    :return:
    """

    escape_seq = {
        '&': '&amp;',
        '<':  '&lt;',
        '>': '&gt;',
    }

    answer = answers[task]

    for k, v in results.items():
        out_file.write('<ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">\n')
        out_file.write('<li class="nav-item">')
        out_file.write('<a class="nav-link active" id="pills-home-tab" data-toggle="pill" href="#trial{0}_{1}" '
                       'role="tab" aria-controls="pills-home" aria-selected="true">'
                       'Trial {1}</a>\n'.format(task+1, k))
        out_file.write('</li>')
        if answer.get(k):
            out_file.write('<li class="nav-item">')
            out_file.write('<a class="nav-link" id="pills-profile-tab" data-toggle="pill" href="#answer{0}_{1}" '
                           'role="tab" aria-controls="pills-profile" aria-selected="false">'
                           'Answer</a>\n'.format(task+1, k))
            out_file.write('</li>')
        out_file.write('</ul>')

        out_file.write('<div class="tab-content" id="pills-tabContent">')
        out_file.write('<div class="tab-pane fade show active" id="trial{0}_{1}" role="tabpanel" '
                       'aria-labelledby="pills-home-tab">'.format(task+1, k))
        
        if v.get('stderr'):
            out_file.write('<pre class="prettyprint linenums">\n')
            for o, n in escape_seq.items():
                v['stderr'] = v['stderr'].replace(o, n)
            out_file.write('{}\n'.format(v['stderr']))
            out_file.write('</pre>\n')
        if v.get('std'):
            out_file.write('<pre class="prettyprint linenums">\n')
            for o, n in escape_seq.items():
                v['std'] = v['std'].replace(o, n)
            out_file.write('{}\n'.format(v['std']))
            out_file.write('</pre>\n')
        if v.get('file'):
            out_file.write('<pre class="prettyprint linenums">\n')
            for o, n in escape_seq.items():
                v['file'] = v['file'].replace(o, n)
            out_file.write('{}\n'.format(v))
            out_file.write('</pre>\n')
        out_file.write('</div>')

        if answer.get(k):
            out_file.write('<div class="tab-pane fade" id="answer{0}_{1}" role="tabpanel" '
                           'aria-labelledby="pills-profile-tab">'.format(task+1, k))
            if answer[k].get('std'):
                out_file.write('<pre class="prettyprint linenums">\n')
                for o, n in escape_seq.items():
                    answer[k]['std'] = answer[k]['std'].replace(o, n)
                out_file.write('{}\n'.format(answer[k]['std']))
                out_file.write('</pre>\n')
            if answer[k].get('file'):
                out_file.write('<pre class="prettyprint linenums">\n')
                for o, n in escape_seq.items():
                    answer[k]['file'] = answer[k]['file'].replace(o, n)
                out_file.write('{}\n'.format(v))
                out_file.write('</pre>\n')
            out_file.write('</div>')
        out_file.write('</div>')


def write_error_msg(msg, out_file):
    """

    :param msg: path to source file
    :param out_file: 書き込みファイル
    :return:
    """

    escape_seq = {
        '&': '&amp;',
        '<':  '&lt;',
        '>': '&gt;',
    }

    out_file.write('<h5>Compile Message</h5>\n')
    out_file.write('<pre class="prettyprint linenums">\n')
    for o, n in escape_seq.items():
        msg = msg.replace(o, n)
    out_file.write('{}\n'.format(msg))
    out_file.write('</pre>\n')


def save_pptx_as_pdf():
    pass


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
        cmd.extend(['-o', out, src])
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
            cmd = ['./' + program]
            result = execute(cmd, desc='Exercise: %d Trial: %d' % (self.ex_num, i+1), shell=True)
            if len(self.input_files) > 0:
                output, error = result.communicate(open(self.input_files[i], 'rb').read(), timeout=TIMEOUT_SEC)
            else:
                output, error = result.communicate(timeout=TIMEOUT_SEC)

            # 無限ループ対策
            if result.wait(TIMEOUT_SEC) is None:
                result.kill()
                # プロセス解放待ち
                time.sleep(1)
                out[i+1].update({'std': INF_MESSAGE})
                out[i+1].update({'point': 3})
            else:
                if result.returncode != 0:
                    if result.returncode == -11:
                        error = b'segmentation fault\n'
                    else:
                        error = b'return code %d\n' % result.returncode
                try:
                    out[i+1].update({'std': output.decode('utf-8'), 'stderr': error.decode('utf-8')})
                except Exception as e:
                    print('Check')
                    out[i+1].update({'std': output.decode('shift-jis'), 'stderr': error.decode('utf-8')})

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
        raise FileNotFoundError('No sentences folders in exercise path')
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

            out_file.write('</div><!-- col-md-4 -->\n')
            for path in sorted(glob.glob(os.path.join(exercise_sentences_path, '**'), recursive=True)):
                if re.match('ex[0-9]+_[0-9]+.html', os.path.basename(path)):
                    name = os.path.splitext(os.path.basename(path))[0]
                    out_file.write(MODAL.format(name, read_html_body(path)))

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
