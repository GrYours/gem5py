#-*- coding:utf-8 -*-
import os
import sys, getopt
import re

def find_dir(argv, inputfolder):
    try:
        opts, args = getopt.getopt(argv,"hd:")
    except getopt.GetoptError:
        print 'python main.py -d <folder> -d <folder> ...'
        sys.exit(2)

    for opt, arg in opts:
        #根据需要可以再添加参数！
        if opt == '-h':
            print 'python main.py -d <folder> -d <folder> ...'
            print 'such as l1size16kB...'
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

def getdata_fromfile(sim_dict, inputfolder):
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
                    item = re.findall(r'(\S+)\s+(\d+[.]{0,1}\d+)\s+(#\s.+)\n', context) # sim_seconds   0.005073   # Number of seconds simulated
                    #print item
                    if item == []:
                        item = re.findall(r'(\S+)\s+(\d+)\s+(#\s.+)\n', context) # sim_seconds   1   # Number of seconds simulated
                        if item == []:
                            # system.mem_ctrls.bytes_read::switch_cpus.data       786960   40.00%      60.00%      # Number of bytes read from this memory
                            item = re.findall(r'(\S+)\s+(\d+[.]{0,1}\d+)\s+(\d+[.]{0,1}\d+%)\s+(\d+[.]{0,1}\d+%)\s+(#\s.+)\n{0,1}', context)
                            if item != []:
                                index_temp[item[0][0]] = float(item[0][1])
                                index_temp[item[0][0]+'_pdf'] = item[0][2]  # pdf
                                index_temp[item[0][0]+'_cdf'] = item[0][3]  # cdf
                        else:
                            index_temp[item[0][0]] = int(item[0][1])
                    else:
                        index_temp[item[0][0]] = float(item[0][1])   #注释没有建立dict，这个之后再说      
                #print index_temp
                bench_index_temp[bench_name] = index_temp
                f.close()
        #print bench_index_temp
        sim_dict[sim_name] = bench_index_temp
