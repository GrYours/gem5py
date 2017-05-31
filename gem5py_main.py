#-*- coding:utf-8 -*-
import sys
import json
import process_file
# import plot_line

inputfolder = []
sim_dict = {}          # 通过dict进行记录，方便查询, sim_dict[sim_name][bench_name][value_name] or 
                       # sim_dict[sim_name][bench_name][name+pdf or name+cdf]

def main(argv):
    process_file.find_dir(argv, inputfolder)
    process_file.getdata_fromfile(sim_dict, inputfolder)

    # write dict to jsonfile.json
    jsObj = json.dumps(sim_dict)   
    fileObject = open('output_jsonFile.json', 'w')  
    fileObject.write(jsObj)  
    fileObject.close()  
    
    #do a test!
    # valuename  = 'system.cpu.dcache.overall_miss_rate::total'
    # plot_line.plot_2D_single(decode_json, valuename)
            
if __name__ == "__main__": 
    main(sys.argv[1:])
