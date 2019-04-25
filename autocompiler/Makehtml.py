#!/usr/bin/python3
# coding: utf-8
"""
Original author : 平野雅也

"""

import traceback
import subprocess
from subprocess import PIPE
import glob
import os
import re


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

def execution(args, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=False, desc=''):
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


def write_code(src, out_file, NKF_BIN):
    """
    コードの内容をファイルに書き出す
    :param src: path to source file
    :param out_file: 書き込みファイル
    :return:
    """

    escape_seq = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
    }

    out_file.write('<pre class="prettyprint linenums">\n')

    ret = False

    try:
        convert = execution([NKF_BIN, '-w', '--overwrite', src])
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
        '<': '&lt;',
        '>': '&gt;',
    }

    answer = answers[task]

    for k, v in results.items():
        out_file.write('<ul class="nav nav-pills mb-3" id="pills-tab" role="tablist">\n')
        out_file.write('<li class="nav-item">')
        out_file.write('<a class="nav-link active" id="pills-home-tab" data-toggle="pill" href="#trial{0}_{1}" '
                       'role="tab" aria-controls="pills-home" aria-selected="true">'
                       'Trial {1}</a>\n'.format(task + 1, k))
        out_file.write('</li>')
        if answer.get(k):
            out_file.write('<li class="nav-item">')
            out_file.write('<a class="nav-link" id="pills-profile-tab" data-toggle="pill" href="#answer{0}_{1}" '
                           'role="tab" aria-controls="pills-profile" aria-selected="false">'
                           'Answer</a>\n'.format(task + 1, k))
            out_file.write('</li>')
        out_file.write('</ul>')

        out_file.write('<div class="tab-content" id="pills-tabContent">')
        out_file.write('<div class="tab-pane fade show active" id="trial{0}_{1}" role="tabpanel" '
                       'aria-labelledby="pills-home-tab">'.format(task + 1, k))

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
                           'aria-labelledby="pills-profile-tab">'.format(task + 1, k))
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
        '<': '&lt;',
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

def create_html(output_dir,student_id, student_ids):
    prev, program_info = None, None
    with open(os.path.join(output_dir, '{}_{}.html'.format('out', student_id)), 'w') as out_file:
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
                '</li>\n'.format(i + 1, '' if i > 0 else 'active')
            )
        out_file.write('</ul>\n')
        out_file.write('<div class="tab-content">\n')
        for i, compiler in enumerate(compilers):
            ret = False
            results = {}

            if i > 0:
                out_file.write('</div>  <!-- tab{}-->\n'.format(i))
            out_file.write('<div id="ex{}" class="tab-pane {}">\n'.format(i + 1, '' if i > 0 else 'active'))
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