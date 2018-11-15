#!/usr/bin/python3
# coding: utf-8
"""
Original author : 平野雅也

"""

import glob
import os
import subprocess
from subprocess import PIPE
import time
import traceback

# 無限ループを判定する猶予
TIMEOUT_SEC = 1
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
            convert = execution(cmd)
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
        result = execution(cmd)
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
            result = execution(cmd, desc='Exercise: %d Trial: %d' % (self.ex_num, i+1), shell=True)
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
