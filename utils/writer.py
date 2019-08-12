import sys
import traceback
from utils.japanese_converter import zen2han
from utils.score_calculation import *
from utils.tools import execute

# nkf のインストールが必要な場合あり，ディレクトリは環境依存
if sys.platform == 'cygwin':
    NKF_BIN = './bin/nkf32.exe'
else:
    NKF_BIN = 'nkf'

# if initially &amp; is used, default replace method makes incorrect text
def replace_seq(text):

    escape_seq = {
        '&': '&amp;',
        '<':  '&lt;',
        '>': '&gt;',
    }

    for o, n in escape_seq.items():
        text = text.replace(n, o)

    for o, n in escape_seq.items():
        text = text.replace(o, n)

    return text


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

    out_file.write('<pre class="prettyprint linenums">\n')

    ret = False
    code_len = 0

    try:
        convert = execute([NKF_BIN, '-w', '--overwrite', src])
        stdout, stderr = convert.communicate()
        with open(src, 'r') as f:
            for line in f.readlines():
                line = replace_seq(line)
                out_file.write(line)
                code_len += len(line)

    except Exception as e:
        print(e)
        traceback.print_exc()

    out_file.write('</pre>\n')
    out_file.write('<!-- class="code length" code length '+ str(code_len) +" -->")

    return ret


def write_trials(results, answers, task, out_file):
    """
    :param results: path to source file
    :param answers: path to source file
    :param task:
    :param out_file: 書き込みファイル
    :return:
    """

    answer = answers[task]
    scores = []
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
            v['stderr'] = replace_seq(zen2han(v['stderr']))
            out_file.write('{}\n'.format(v['stderr']))
            out_file.write('</pre>\n')
        if v.get('std'):
            out_file.write('<pre class="prettyprint linenums">\n')
            v['std'] = replace_seq(zen2han(v['std']))
            out_file.write('{}\n'.format(v['std']))
            out_file.write('</pre>\n')
        if v.get('file'):
            out_file.write('<pre class="prettyprint linenums">\n')
            v['file'] = replace_seq(zen2han(v['file']))
            out_file.write('{}\n'.format(v))
            out_file.write('</pre>\n')
        out_file.write('</div>')

        if answer.get(k):
            out_file.write('<div class="tab-pane fade" id="answer{0}_{1}" role="tabpanel" '
                           'aria-labelledby="pills-profile-tab">'.format(task+1, k))
            if answer[k].get('std'):
                out_file.write('<pre class="prettyprint linenums">\n')
                answer[k]['std'] = replace_seq(zen2han(answer[k]['std']))
                out_file.write('{}\n'.format(answer[k]['std']))
                out_file.write('</pre>\n')
            if answer[k].get('file'):
                out_file.write('<pre class="prettyprint linenums">\n')
                answer[k]['file'] = replace_seq(zen2han(answer[k]['file']))
                out_file.write('{}\n'.format(v))
                out_file.write('</pre>\n')
            out_file.write('</div>')
        out_file.write('</div>')

        if v.get('std'):
            delimiter = select_delimiter(split_string(answer[k]['std']))
            max_score = calc_BLEU(answer[k]['std'], answer[k]['std'], delimiter, 4)
            score = calc_BLEU(v['std'], answer[k]['std'], delimiter, 4)
            #print(score)
            #print(max_score)
            score = score / max_score
            scores.append(score)
            out_file.write("<!-- score "+ str(score) +" -->")
		
    if len(scores) != 0:
        ave_score = sum(scores)/len(scores)
        #print(scores)
        out_file.write('<!-- class="averagescore" average score '+ str(ave_score) +" -->")


def write_error_msg(msg, out_file):
    """
    :param msg: path to source file
    :param out_file: 書き込みファイル
    :return:
    """

    out_file.write('<h5>Compile Message</h5>\n')
    out_file.write('<pre class="prettyprint linenums">\n')
    msg = replace_seq(msg)
    out_file.write('{}\n'.format(msg))
    out_file.write('</pre>\n')