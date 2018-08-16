#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os


# 获取文件件列表
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


if __name__ == '__main__':
    path = '/Users/binny/study/PS/CS6'
    file_list = get_file_list(path)
    file_list = clean_list(file_list)
    # print(file_list)
    # print(len(file_list))
    for res in file_list:
        file_list_1 = get_file_list(res)
        print(res)
        for k in file_list_1:
            if k.find('exe') != -1:
                print(k[0:len(k) - 4])
                name = k[0:len(k) - 4]
                print(res + name)
                try:
                    os.rename(res, res + name)
                except Exception as e:
                    print(repr(e))
