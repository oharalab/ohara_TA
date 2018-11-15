#!/usr/bin/python3
# coding: utf-8
"""
Original author : 平野雅也

"""

import traceback
import subprocess
from subprocess import PIPE

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


def write_code(src, out_file):
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