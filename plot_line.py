#-*- coding:utf-8 -*-
# from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TextInput, Select
from bokeh.plotting import figure

import json

# 个数有限，如果需要更多的线段，需要扩展这个index
color_index = {
    0:'red',
    1:'blue',
    2:'green',
    3:'orange',
    4:'black',
    5:'yellow'
}

file_input=open('output_jsonFile.json', 'r')
sim_obj = json.load(file_input, encoding='utf-8')
file_input.close()

sim_name_list = []
bench_name_list = []
y_plot = {}

for simname in sim_obj:
    sim_name_list.append(simname)

for simname in sim_obj:
    for benchname in sim_obj[simname]:
        bench_name_list.append(benchname)
    break

sim_name = Select(value='l1size2kB', options=sim_name_list)     # you can select what you want.But it has not complete
bench_name = Select(value='bcnt', options=bench_name_list)
value_name = TextInput(title="value_name", value='sim_seconds')


plot = figure(tools="pan,box_zoom,reset,save", 
        title=value_name.value,
        x_range=bench_name_list, 
        x_axis_label='bench_name', y_axis_label='value'
    )

i = 0
for simname in sim_obj:
    y = []
    for benchname in sim_obj[simname]:
        y.append(sim_obj[simname][benchname][value_name.value])
    y_plot[i] = y
    globals()['source'+str(i)] = ColumnDataSource(data=dict(x=bench_name_list, y=y_plot[i]))        #定义source，这个很重要
    plot.line(bench_name_list, y_plot[i], source=globals()['source'+str(i)], legend=sim_name_list[i], line_width=3, line_color=color_index[i])
    i += 1

# Set up callbacks
def update_value_name(attrname, old, new):
    plot.title.text = value_name.value

    i = 0
    for simname in sim_obj:
        y = []
        for benchname in sim_obj[simname]:
            y.append(sim_obj[simname][benchname][value_name.value])
        y_plot[i] = y
        globals()['source'+str(i)].data = dict(x=bench_name_list, y=y_plot[i])       #update data
        i += 1
    
value_name.on_change('value', update_value_name)

input_text = widgetbox(sim_name, bench_name, value_name)
curdoc().add_root(row(input_text, plot, width=1600))
curdoc().title = "Lines"


# def plot_2D_single(sim_obj, valuename):
#     # output to static HTML file
#     output_file(valuename+'_lines.html')
#     bench = []
#     for sim_name in sim_obj:
#         for bench_name in sim_obj[sim_name]:
#             bench.append(bench_name)
#         break

#     # create a new plot with a title and axis labels
#     #必须要设置x_range,否则当x为字符时输出是一个空图像
#     p = figure(tools="pan,box_zoom,reset,save", 
#         title=valuename,
#         x_range=bench, 
#         x_axis_label='bench_name', y_axis_label='value'
#     )

#     i = 0
#     for sim_name in sim_obj:
#         y = []
#         for bench_name in sim_obj[sim_name]:
#             #print sim_obj[sim_name][bench_name][valuename]
#             y.append(sim_obj[sim_name][bench_name][valuename])
#         p.line(bench, y, legend=sim_name, line_width=3, line_color=color_index[i])
#         i += 1
#     # show the results
#     show(p)
