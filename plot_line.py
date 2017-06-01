#-*- coding:utf-8 -*-
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, PreText, MultiSelect, Toggle, Button, DataTable, TableColumn
from bokeh.plotting import figure

import json
import pandas as pd
import numpy as np
import re

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
value_name_mul = MultiSelect(title="value_name_mul", value=['sim_seconds','sim_ticks'], options=value_name_list)
real_value = PreText(text='real_value: 0')
samesim_diffbench_average = PreText(text='samesim_diffbench_average: 0')
toggle = Toggle(label='Active!', active=False)
button = Button(label='OK!') 

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


table_data = dict(
        valuename_s=['None']*10,
        value_s=['None']*10,
        value_cdf=['None']*10,
        value_pdf=['None']*10,
    )
table_source = ColumnDataSource(table_data)

columns = [
        TableColumn(field="valuename_s", title="Valuename", width=800),
        TableColumn(field="value_s", title="Value"),
        TableColumn(field="value_cdf", title="Value_cdf"),
        TableColumn(field="value_pdf", title="Value_pdf"),
    ]
table = DataTable(source=table_source, columns=columns, width=800)


def update_test():
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

    if toggle.active == True:
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
            plot1.line(value_name_mul.value, y_plot1[i], legend=bench_name_list[i], line_width=3, line_color=color_index[i])
            i += 1

        curdoc().add_root(plot1)
        # curdoc().remove_root(plot1, setter=None) # 怎么删，头疼

    # 截取:号前的部分
    value_name_temp = ''
    for str_t in value_name.value:
        if str_t == ':':
            break
        value_name_temp = value_name_temp + str_t
    # print value_name_temp
    value_name_table = []
    value_table = []
    value_table_cdf = {}
    value_table_pdf = {}
    for valuename in value_name_list:
        if re.match(value_name_temp+'\S+'+'_cdf', valuename):
            valuename_nocdf = valuename[:-4]
            # print valuename_nocdf     
            value_table_cdf[valuename_nocdf] = sim_obj[sim_name.value][bench_name.value][valuename]
        elif re.match(value_name_temp+'\S+'+'_pdf', valuename):
            valuename_nopdf = valuename[:-4]
            # print valuename_nopdf
            value_table_pdf[valuename_nopdf] = sim_obj[sim_name.value][bench_name.value][valuename]
        elif re.match(value_name_temp+'\S+', valuename):
            # print valuename
            value_name_table.append(valuename)
            value_table.append(sim_obj[sim_name.value][bench_name.value][valuename])

    value_table_cdf_list = []
    value_table_pdf_list = []
    for valuename in value_name_table:
        if valuename in value_table_cdf:
            value_table_cdf_list.append(value_table_cdf[valuename])
        else:
            value_table_cdf_list.append('None')
        if valuename in value_table_pdf:
            value_table_pdf_list.append(value_table_cdf[valuename])
        else:
            value_table_pdf_list.append('None')
    
    table_source.data = dict(
        valuename_s=value_name_table,
        value_s=value_table,
        value_cdf=value_table_cdf_list,
        value_pdf=value_table_pdf_list,
    )

button.on_click(update_test)

##############################################
input_text = widgetbox(sim_name, 
    bench_name, 
    value_name, 
    real_value,
    value_name_mul, 
    samesim_diffbench_average, 
    toggle,
    button,
    table,
    width = 800)

curdoc().add_root(row(input_text, plot0))
curdoc().title = "Lines"

