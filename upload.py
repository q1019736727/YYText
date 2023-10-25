#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/17
# @Author  : cy
# @Site    :
# @File    : upload.py
# @Software: PyCharm

import os
import subprocess
import time
import datetime


def upload():
    commitMsg = input('请输入提交信息:   ')
    if len(commitMsg) <= 0:
        print('未输入提交信息，load失败')
        return

    commitTag = input('请输入提交版本号:   ')
    if len(commitTag) <= 0:
        print('未输入版本号，load失败')
        return

    gitaddCode = execute_command('git add .')
    if gitaddCode != 200:
        return
    gitcommitCode = execute_command('git commit -m ' + commitMsg)
    if gitcommitCode != 200:
        return
    gitpushCode = execute_command('git push')
    if gitpushCode != 200:
        return
    gittagCode = execute_command('git tag ' + commitTag)
    if gittagCode != 200:
        return
    gittagpushCode = execute_command('git push --tags')
    if gittagpushCode != 200:
        return
    agenCode = addagent()
    if agenCode != 200:
        return
    os.system('pod trunk push  --verbose  --allow-warnings')
    print('pod库上传成功')

def addagent():
    agentString = 'export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890'
    result = execute_command(agentString)
    return result

def podtrunk():
    print('开始上传pod')
    trunkString = 'pod trunk push  --verbose  --allow-warnings'
    result = execute_command(trunkString)
    return result

def execute_command(cmdstring=''):
    if len(cmdstring) <= 0:
        print('请输入命令')
        return 0
    #超时180秒
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=180)

    sub = subprocess.Popen(cmdstring, shell=True, stdout=subprocess.PIPE, bufsize=4096)
    while True:
        if sub.poll() is not None:
            break
        time.sleep(0.1)
        if end_time <= datetime.datetime.now():
            sub.kill()
            print('执行命令超时')
            return 0

    if sub.returncode == 0:
        print("执行成功 " + cmdstring)
        return 200
    else:
        print("执行失败 " + cmdstring)
        return 0

if __name__=='__main__':
    upload()