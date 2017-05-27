#-*- coding:utf-8 -*-
import os
import sys, getopt
import re

inputfolder = []
bench_name = []

def find_dir(argv):
    try:
        opts, args = getopt.getopt(argv,"hd:")
    except getopt.GetoptError:
        print 'python main.py -d <folder> -d <folder> ...'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python main.py -d <folder> -d <folder> ...'
            print 'such as l1size16kB'
            print 'python main.py -d .    Can get all folder in this catalog!'
            sys.exit()
        elif opt == '-d':
            if arg == '.':
                cur_path = os.getcwd()     #当前目录
                get_dir = os.listdir(cur_path)  #遍历当前目录，获取文件列表
                for sub_dir in get_dir:
                    if os.path.isdir(sub_dir):     #如果当前是文件夹
                        inputfolder.append(sub_dir)
            else:
                inputfolder.append(arg)
    print '文件夹为：', inputfolder

def main(argv):
    find_dir(argv)
    for dirs in inputfolder:
        path = os.path.join('.', dirs)
        for files in os.listdir(path): 
            if os.path.splitext(files)[1] == '.stats':  #只打开.stats格式的文件
                bench_name.append(os.path.splitext(files)[0]) #bench name
                files = os.path.join(dirs, files)       #要加上路径
                f = open(files, 'r')

                guid = f.readlines()[2]
                print guid

                f.close()
            
if __name__ == "__main__": 
    main(sys.argv[1:])
