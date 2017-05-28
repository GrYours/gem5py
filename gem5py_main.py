#-*- coding:utf-8 -*-
import os
import sys
import re
#import numpy as np    #等矩阵处理的时候再考虑
import process_file
import plot_line

inputfolder = []
sim_dict = {}          #通过dict进行记录，方便查询

def main(argv):
    process_file.find_dir(argv, inputfolder)
    process_file.getdata_fromfile(sim_dict, inputfolder)
    
    #do a test!
    valuename  = 'system.cpu.dcache.overall_miss_rate::total'
    plot_line.plot_2D_single(sim_dict, valuename)
    plot_line.plot_2D_single_vector(sim_dict, valuename)
            
if __name__ == "__main__": 
    main(sys.argv[1:])
