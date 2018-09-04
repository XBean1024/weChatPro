#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import math
import os

# 获取文件件列表
import shutil

from twisted.python.util import println


def get_file_list(path_p):
    file = os.path.exists(path_p)
    if not file:
        print('文件不存在' + path_p)
        return
    file_list_l = os.listdir(path_p)  # 文件列表
    return file_list_l


# 打印文件路径
def print_file_path(file_p):
    for i in file_p:
        p = path + '/' + i
        print(p)


# 清理文件列表
def clean_list(file_p):
    l = []
    for i in file_p:
        p = path + '/' + i
        if p.find('.') == -1:
            l.append(p)

    return l


# 文件夹重命名
def rename_dir(file_list_p):
    for res in file_list_p:
        file_list_1 = get_file_list(res)
        # print(res)
        for k in file_list_1:
            if k.find('exe') != -1:
                print(k[0:len(k) - 4])
                name = k[0:len(k) - 4]
                print(res + name)
                try:
                    os.rename(res, res + name)
                except Exception as e:
                    print(repr(e))


# 文件移除
def remove_file(file_list_p):
    for res in file_list_p:
        file_list_1 = get_file_list(res)
        # print(res)
        for k in file_list_1:
            if k.find('exe') == -1:
                print(res + k)
                try:
                    os.remove(res + k)
                except Exception as e:
                    print(repr(e))


# 文件重命名
def rename_file(path_p, list_p):
    length = len(path_p)
    print(length)
    for res in list_p:
        fl = os.listdir(res)
        for f in fl:
            print("文件夹 ：" + res[26:] + " === 文件：" + res + '/' + f)
            # folder_name = res[26:]
            # file_path = res + '/' + f

            # os.rename(res + '/' + f, res + '/' + folder_name+'.exe')
            shutil.move(res + '/' + f, path_p)


if __name__ == '__main__':
    path = '/Users/binny/study/PS/CS6'
    # file_list = get_file_list(path)
    # dir_list = clean_list(file_list)
    # print(len(file_list))

    # rename_dir(dir_list)
    # rename_file(path, dir_list)
    # print(file_list)
    # for f in file_list:
    #     if f.find("exe") == -1:
    #         print(path + '/' + f)
    #         # os.remove(path + '/' + f)
    sums = 300
    check = 1.003
    checks = 0
    for i in range(1, 241):
        sums = sums * 1.003 + 300
        checks = checks + math.pow(check, i)
        println(i)
        println(checks * 300)
    println(sums)
