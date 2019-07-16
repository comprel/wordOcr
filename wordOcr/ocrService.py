#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import sys
from conf.config import GeneralFilePath, SAVEFILE
from core.ocrImageGenery import BasicImageGenery


def CollectService():
    if GeneralFilePath:
        print "警告: 文件夹及文件路径不要使用中文"
        filepath = GeneralFilePath.replace("\\", "/")
        ocr = BasicImageGenery()
        if not os.path.exists(filepath):
            print "文件路径 %s 不存在" % filepath
        if os.path.isfile(filepath):
            ocr.general_one(filepath)
        elif os.path.isdir(filepath):
            ocr.general_path(filepath)
        else:
            print "未识别的文件路径"
            sys.exit(2)
        print "图片识别完成，请在 %s 中查看" % SAVEFILE
    else:
        print "请在conf文件下配置GeneralFilePath 指定分析文件路径或目录"
        sys.exit(1)
