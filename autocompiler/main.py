#!/usr/bin/python3
# coding: utf-8
"""
Original author : 平野雅也

"""

import collections
import datetime
import glob
import os
import re
import shutil
import sys
import traceback
import zipfile
import argparse


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


