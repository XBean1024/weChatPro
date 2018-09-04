#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import shutil

from twisted.python.util import println


def get_files(dir_p, delete_file):
    file_list = os.listdir(dir_p)
    i = 0
    for count, file_child in enumerate(file_list):
        dir_1 = dir_p + "/" + file_child
        fl = os.path.isdir(dir_1)
        if fl:
            if file_child == 'build':
                println(dir_1)
                shutil.rmtree(dir_1)  # 删除非空目录
            else:
                get_files(dir_1)


if __name__ == "__main__":
    # 遍历某一目录下的所所有文件
    dir = '/Users/binny/AndroidStudioProjects'
    get_files(dir, 'build')
