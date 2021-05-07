#!/usr/bin/env python        可以让这个py文件直接在Unix/Linux/Mac上运行
# -*- coding: utf-8 -*-      使用标准UTF-8编码；

# ' main entry point '            #表示模块的文档注释
import argparse

__author__ = 'Song Hui'  # 作者名

import sys


def get_options():
    # Initialize parser
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-p", "--project", help="Use specified project file")

    # Read arguments from command line
    args = parser.parse_args()

    if args:
        print("parsing arguments: {}".format(args))
    return {'project': args.project}


if __name__ == '__main__':
    option = get_options()
