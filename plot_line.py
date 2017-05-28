#-*- coding:utf-8 -*-
from bokeh.plotting import figure, output_file, show

# 个数有限，如果需要更多的线段，需要扩展这个index
color_index = {
    0:'red',
    1:'blue',
    2:'green',
    3:'orange',
    4:'black',
    5:'yellow'
}

def plot_2D_single(sim_obj, valuename):
    # output to static HTML file
    output_file(valuename+'_lines.html')
    bench = []
    for sim_name in sim_obj:
        for bench_name in sim_obj[sim_name]:
            bench.append(bench_name)
        break

    # create a new plot with a title and axis labels
    #必须要设置x_range,否则当x为字符时输出是一个空图像
    p = figure(tools="pan,box_zoom,reset,save", 
        title=valuename,
        x_range=bench, 
        x_axis_label='bench_name', y_axis_label='value'
    )

    i = 0
    for sim_name in sim_obj:
        y = []
        for bench_name in sim_obj[sim_name]:
            #print sim_obj[sim_name][bench_name][valuename]
            y.append(sim_obj[sim_name][bench_name][valuename])
        p.line(bench, y, legend=sim_name, line_width=3, line_color=color_index[i])
        i += 1
    # show the results
    show(p)

def plot_2D_single_vector(sim_obj, valuename):
    
