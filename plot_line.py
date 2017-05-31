#-*- coding:utf-8 -*-
# from bokeh.plotting import figure, output_file, show
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TextInput, Select, PreText, MultiSelect
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
value_name_list = []

for simname in sim_obj:
    sim_name_list.append(simname)

for simname in sim_obj:
    for benchname in sim_obj[simname]:
        bench_name_list.append(benchname)
    break

for simname in sim_obj:
    for benchname in sim_obj[simname]:
        for valuename in sim_obj[simname][benchname]:
            value_name_list.append(valuename)
        # print sim_obj[simname][benchname]['system.switch_cpus.op_class::FloatAdd_cdf']
        break
    break    
value_name_list.sort()
##############################################

sim_name = Select(title="sim_name", value='l1size2kB', options=sim_name_list)     # you can select what you want.But it has not complete
bench_name = Select(title="bench_name", value='bcnt', options=bench_name_list)
# value_name = TextInput(title="value_name", value='sim_seconds')
value_name = Select(title="value_name", value='sim_seconds', options=value_name_list)
real_value = PreText(text='real_value: 0')
samesim_diffbench_average = PreText(text='samesim_diffbench_average: 0')
# samesim_diffbench_max = PreText(text='samesim_diffbench_max: 0')
# samesim_diffbench_min = PreText(text='samesim_diffbench_min: 0')

plot0 = figure(tools="pan,box_zoom,reset,save", 
        title=value_name.value,
        x_range=bench_name_list, 
        x_axis_label='bench_name', y_axis_label='value'
    )

y_plot0 = {}
i = 0
for simname in sim_obj:
    y = []
    for benchname in sim_obj[simname]:
        y.append(sim_obj[simname][benchname][value_name.value])
    y_plot0[i] = y
    globals()['source0'+str(i)] = ColumnDataSource(data=dict(x=bench_name_list, y=y_plot0[i]))        # 定义source，这个很重要
    plot0.line(bench_name_list, y_plot0[i], source=globals()['source0'+str(i)], legend=sim_name_list[i], line_width=3, line_color=color_index[i])
    i += 1

# updata value and avg
def update_stats():
    real_value.text = 'real_value: '+str(sim_obj[sim_name.value][bench_name.value][value_name.value])
    avg = 0
    for benchname in bench_name_list:
        avg = avg + sim_obj[sim_name.value][benchname][value_name.value]
    avg = avg / len(bench_name_list)
    samesim_diffbench_average.text = 'samesim_diffbench_average: '+str(avg)

# Set up callbacks
def update_value_name(attrname, old, new):
    update_stats()
    plot0.title.text = value_name.value
    i = 0
    for simname in sim_obj:
        y = []
        for benchname in sim_obj[simname]:
            y.append(sim_obj[simname][benchname][value_name.value])
        y_plot0[i] = y
        globals()['source0'+str(i)].data = dict(x=bench_name_list, y=y_plot0[i])       # update data
        i += 1

for w in [value_name, sim_name, bench_name]:
    w.on_change('value', update_value_name)    
# value_name.on_change('value', update_value_name)

##############################################
value_name_mul = MultiSelect(title="value_name_mul", value=['sim_seconds','sim_ticks'], options=value_name_list)

plot1 = figure(tools="pan,box_zoom,reset,save", 
        title=sim_name.value,
        x_range=value_name_mul.value, 
        x_axis_label='value_name', y_axis_label='value'
    )

y_plot1 = {}
i = 0
for benchname in bench_name_list:
    y = []
    for valuename in value_name_mul.value:
        y.append(sim_obj[sim_name.value][benchname][valuename])
    y_plot1[i] = y
    globals()['source1'+str(i)] = ColumnDataSource(data=dict(x=value_name_mul.value, y=y_plot1[i]))
    plot1.line(value_name_mul.value, y_plot1[i], source=globals()['source1'+str(i)], legend=bench_name_list[i], line_width=3, line_color=color_index[i])
    i += 1

# Set up callbacks
def update_plot1(attrname, old, new):
    plot1.title.text = sim_name.value
    plot1.x_range = value_name_mul.value
    i = 0
    for benchname in bench_name_list:
        y = []
        for valuename in value_name_mul.value:
            y.append(sim_obj[sim_name.value][benchname][valuename])
        y_plot1[i] = y
        globals()['source1'+str(i)].data = dict(x=value_name_mul.value, y=y_plot1[i])
        i += 1
    
value_name_mul.on_change('value', update_plot1)

##############################################
input_text = widgetbox(sim_name, bench_name, value_name, value_name_mul,
            real_value, samesim_diffbench_average)

curdoc().add_root(row(input_text, plot0, plot1))
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
