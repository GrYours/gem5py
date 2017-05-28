#-*- coding:utf-8 -*-
import os
import sys, getopt
import re
#import numpy as np    #等矩阵处理的时候再考虑
import plot_line

inputfolder = []
#bench_name = []
sim_dict = {}  #通过dict进行记录，方便查询

def find_dir(argv):
    try:
        opts, args = getopt.getopt(argv,"hd:")
    except getopt.GetoptError:
        print 'python main.py -d <folder> -d <folder> ...'
        sys.exit(2)

    for opt, arg in opts:
        #根据需要可以再添加参数！
        if opt == '-h':
            print 'python main.py -d <folder> -d <folder> ...'
            print 'such as l1size16kB'
            print 'python main.py -d .    Can get all folder in this catalog!'
            sys.exit()
        elif opt == '-d':
            if arg == '.':
                cur_path = os.getcwd()           #当前目录
                get_dir = os.listdir(cur_path)   #遍历当前目录，获取文件列表
                for sub_dir in get_dir:
                    if os.path.isdir(sub_dir):   #如果当前是文件夹
                        if sub_dir != '.git':    #其他类型的文件夹这里没有进行过滤处理
                            inputfolder.append(sub_dir)
            else:
                inputfolder.append(arg)

    print '文件夹为：', inputfolder

def main(argv):
    find_dir(argv)

    for sim_name in inputfolder:
        bench_index_temp = {} 
        path = os.path.join('.', sim_name)
        for files in os.listdir(path): 
            if os.path.splitext(files)[1] == '.stats':        #只打开.stats格式的文件
                bench_name = os.path.splitext(files)[0]       #bench name
                files = os.path.join(sim_name, files)         #要加上路径
                f = open(files, 'r')
                index_temp = {}
                for context in f.readlines()[2:1037]:
                    #print contexts
                    item = re.findall(r'(\S+)\s+(\d+[.]{0,1}\d+)\s+(#\s.+)\n', context)
                    #print item
                    if item == []:
                        #print 'None!Waiting me to deal with it!'
                        no = 1
                    else:
                        index_temp[item[0][0]] = float(item[0][1])   #注释没有建立dict，这个之后再说
                    
                #print index_temp
                bench_index_temp[bench_name] = index_temp
                f.close()
        #print bench_index_temp
        sim_dict[sim_name] = bench_index_temp
    #do a test!
    #sim_name0   = 'l2size64kB'
    #bench_name0 = 'bcnt'
    valuename  = 'system.cpu.dcache.overall_miss_rate::total'
    plot_line.plot_2D_single(sim_dict, valuename)
    # for i0 in sim_dict:
    #     for i1 in sim_dict[i0]:
    #         print i1
            
if __name__ == "__main__": 
    main(sys.argv[1:])
