import glob
import os
import zipfile

def get_students(student_file):
    students = {}
    with open(student_file) as f:
        for line in f.readlines():
            s, n = line.strip().split(' ')
            students[s] = n
    return students


def unzip_sentences_files(exercise_sentences_path):
    exercise_sentences_files = glob.glob(os.path.join(exercise_sentences_path, '*'))
    if len(exercise_sentences_files) == 1:
        filename = exercise_sentences_files[0]
        if os.path.splitext(filename)[1] == '.zip':
            with zipfile.ZipFile(filename) as zfile:
                zfile.extractall(path=exercise_sentences_path)
    elif len(exercise_sentences_files) < 1:
        raise FileNotFoundError('No files in exercise path')


def read_html_answer(filename, encoding="utf8"):
    with open(filename, 'r', encoding=encoding, errors="ignore")as f:
        result = f.read()
    #print(result)
    return result


def read_html_body(filename, encoding="utf8"):
    with open(filename, 'r', encoding="utf8") as f:#encoding="shift-jis") as f:
        html_data = f.read().encode(encoding, errors="ignore").decode(encoding, errors="ignore")
    _, html_data = html_data.split('<body')
    idx = html_data.find('>') + 1
    html_data, _ = html_data[idx:].split('</body')
    if "<div class=\"result\">" in html_data and "</div>" not in html_data:
        html_data += "</div>"
    #print(html_data)
    return html_data
