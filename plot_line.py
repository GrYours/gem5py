#-*- coding:utf-8 -*-
from bokeh.io import curdoc
from bokeh.layouts import row, column, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Select, PreText, MultiSelect, Toggle, Button, DataTable, TableColumn, RadioGroup
from bokeh.plotting import figure

import json
import re
import pandas as pd
import numpy as np

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
        break
    break    
value_name_list.sort()

value_simple = []
for valuename in value_name_list:
    value_name_temp = ''
    for str_t in valuename: 
        value_name_temp = value_name_temp + str_t
        if str_t == ':':
            break
    value_simple.append(value_name_temp)
value_simple = list(set(value_simple))
value_simple.sort()
##############################################

sim_name = MultiSelect(title="sim_name", value=[sim_name_list[0]], options=sim_name_list)     # you can select what you want.But it has not complete
bench_name = MultiSelect(title="bench_name", value=[bench_name_list[0]], options=bench_name_list)
value_name = Select(title="value_name", value='system.switch_cpus.ipc', options=value_simple)
toggle_plot = Toggle(label='Active plot!', active=False)
toggle_table = Toggle(label='Active table!', active=False)
# button = Button(label='OK!')   
radio_group = RadioGroup(
        labels=["scalar", "vector_samesim", "vector_samebench"], active=0)

radio_for_vector = RadioGroup(
        labels=["value", "cdf", "pdf"], active=0)

radio_for_csv = RadioGroup(
        labels=["createCSV", "NotCreateCSV"], active=0)

def togglePlotCallback(attr):
    # Get the layout object added to the documents root
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children

    valuename_table = []
    valuenamecdf_table = []
    valuenamepdf_table = []
    for valuename in value_name_list:
        if re.match(value_name.value+'\S+'+'_cdf', valuename):
            valuenamecdf_table.append(valuename)    
        elif re.match(value_name.value+'\S+'+'_pdf', valuename):
            valuenamepdf_table.append(valuename) 
        elif re.match(value_name.value+'\S+', valuename) or re.match(value_name.value, valuename):
            valuename_table.append(valuename)

    if radio_group.active == 0: # for scalar
        # Either add or remove the second graph
        if toggle_plot.active == False:
            plotToRemove = curdoc().get_model_by_name('plot0')
            listOfSubLayouts.remove(plotToRemove)

        if toggle_plot.active == True:
            if not curdoc().get_model_by_name('plot0'):
                plot0 = figure(
                    name='plot0', 
                    title=value_name.value,
                    x_range=bench_name.value, 
                    x_axis_label='bench_name', 
                    y_axis_label='value'
                )
                plotToAdd = plot0
                y_plot0 = {}
                i = 0
                for simname in sim_name.value:
                    y = []
                    for benchname in bench_name.value:
                        y.append(sim_obj[simname][benchname][value_name.value])
                    y_plot0[simname] = y
                    print bench_name.value
                    plot0.line(bench_name.value, y_plot0[simname], legend=simname, line_width=3, line_color=color_index[i])
                    i += 1
            else:
                plotToAdd = curdoc().get_model_by_name('plot0')
            listOfSubLayouts.append(plotToAdd)

    elif radio_group.active == 1: #for vector samesim
  
        if radio_for_vector.active == 0:  # for value
            if toggle_plot.active == False:
                plotToRemove = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.remove(plotToRemove)

            if toggle_plot.active == True:
                if not curdoc().get_model_by_name('plot0'): 
                    # make valuename short
                    valuename_short = []
                    count = 0
                    for valuename in valuename_table:
                        valuename_temp1 = ''
                        for str_t in valuename:
                            if count == 2:
                                valuename_temp1 = valuename_temp1 + str_t
                            if str_t == ':': 
                                count += 1
                        count = 0
                        valuename_short.append(valuename_temp1) 

                    plot0 = figure(
                        name='plot0', 
                        title=sim_name.value[0],
                        x_range=valuename_short, 
                        x_axis_label='value_vector', 
                        y_axis_label='value',
                        width=1600
                    )
                    plot0.xaxis.major_label_orientation='vertical'
                    plotToAdd = plot0
                    y_plot1 = {}
                    i = 0
                    for benchname in bench_name.value:
                        y = []
                        for valuename in valuename_table:
                            y.append(sim_obj[sim_name.value[0]][benchname][valuename])           
                        y_plot1[benchname] = y
                        plot0.line(valuename_short, y_plot1[benchname], legend=benchname, line_width=3, line_color=color_index[i])
                        i += 1
                else:
                    plotToAdd = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.append(plotToAdd)
       
        elif radio_for_vector.active == 1:  # for cdf
            if toggle_plot.active == False:
                plotToRemove = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.remove(plotToRemove)

            if toggle_plot.active == True:
                if not curdoc().get_model_by_name('plot0'): 
                    # make valuename short
                    valuename_short = []
                    count = 0
                    for valuename in valuenamecdf_table:
                        valuename_temp1 = ''
                        for str_t in valuename:
                            if count == 2:
                                valuename_temp1 = valuename_temp1 + str_t
                            if str_t == ':': 
                                count += 1
                        count = 0
                        valuename_short.append(valuename_temp1[:-4]) 

                    plot0 = figure(
                        name='plot0', 
                        title=sim_name.value[0], 
                        x_range=valuename_short, 
                        x_axis_label='value_vector', 
                        y_axis_label='value',
                        width=1600
                    )
                    plot0.xaxis.major_label_orientation='vertical'
                    plotToAdd = plot0
                    y_plot1 = {}
                    i = 0
                    for benchname in bench_name.value:
                        y = []
                        for valuename in valuenamecdf_table:
                            y.append(sim_obj[sim_name.value[0]][benchname][valuename])           
                        y_plot1[benchname] = y
                        plot0.line(valuename_short, y_plot1[benchname], legend=benchname, line_width=3, line_color=color_index[i])
                        i += 1
                else:
                    plotToAdd = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.append(plotToAdd)

        elif radio_for_vector.active == 2:  # for pdf
            if toggle_plot.active == False:
                plotToRemove = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.remove(plotToRemove)

            if toggle_plot.active == True:
                if not curdoc().get_model_by_name('plot0'): 
                    # make valuename short
                    valuename_short = []
                    count = 0
                    for valuename in valuenamepdf_table:
                        valuename_temp1 = ''
                        for str_t in valuename:
                            if count == 2:
                                valuename_temp1 = valuename_temp1 + str_t
                            if str_t == ':': 
                                count += 1
                        count = 0
                        valuename_short.append(valuename_temp1[:-4]) 

                    plot0 = figure(
                        name='plot0', 
                        title=sim_name.value[0], 
                        x_range=valuename_short, 
                        x_axis_label='value_vector', 
                        y_axis_label='value',
                        width=1600
                    )
                    plot0.xaxis.major_label_orientation='vertical'
                    plotToAdd = plot0
                    y_plot1 = {}
                    i = 0
                    for benchname in bench_name.value:
                        y = []
                        for valuename in valuenamepdf_table:
                            y.append(sim_obj[sim_name.value[0]][benchname][valuename])           
                        y_plot1[benchname] = y
                        plot0.line(valuename_short, y_plot1[benchname], legend=benchname, line_width=3, line_color=color_index[i])
                        i += 1
                else:
                    plotToAdd = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.append(plotToAdd)

    elif radio_group.active == 2: # for vector samebench
        if radio_for_vector.active == 0:  # for value
            if toggle_plot.active == False:
                plotToRemove = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.remove(plotToRemove)

            if toggle_plot.active == True:
                if not curdoc().get_model_by_name('plot0'): 
                    # make valuename short
                    valuename_short = []
                    count = 0
                    for valuename in valuename_table:
                        valuename_temp1 = ''
                        for str_t in valuename:
                            if count == 2:
                                valuename_temp1 = valuename_temp1 + str_t
                            if str_t == ':': 
                                count += 1
                        count = 0
                        valuename_short.append(valuename_temp1) 

                    plot0 = figure(
                        name='plot0', 
                        title=bench_name.value[0],
                        x_range=valuename_short, 
                        x_axis_label='value_vector', 
                        y_axis_label='value',
                        width=1600
                    )
                    plot0.xaxis.major_label_orientation='vertical'
                    plotToAdd = plot0
                    y_plot1 = {}
                    i = 0
                    for simname in sim_name.value:
                        y = []
                        for valuename in valuename_table:
                            y.append(sim_obj[simname][bench_name.value[0]][valuename])           
                        y_plot1[simname] = y
                        plot0.line(valuename_short, y_plot1[simname], legend=simname, line_width=3, line_color=color_index[i])
                        i += 1
                else:
                    plotToAdd = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.append(plotToAdd)
       
        elif radio_for_vector.active == 1:  # for cdf
            if toggle_plot.active == False:
                plotToRemove = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.remove(plotToRemove)

            if toggle_plot.active == True:
                if not curdoc().get_model_by_name('plot0'): 
                    # make valuename short
                    valuename_short = []
                    count = 0
                    for valuename in valuenamecdf_table:
                        valuename_temp1 = ''
                        for str_t in valuename:
                            if count == 2:
                                valuename_temp1 = valuename_temp1 + str_t
                            if str_t == ':': 
                                count += 1
                        count = 0
                        valuename_short.append(valuename_temp1[:-4]) 

                    plot0 = figure(
                        name='plot0', 
                        title=bench_name.value[0], 
                        x_range=valuename_short, 
                        x_axis_label='value_vector', 
                        y_axis_label='value',
                        width=1600
                    )
                    plot0.xaxis.major_label_orientation='vertical'
                    plotToAdd = plot0
                    y_plot1 = {}
                    i = 0
                    for simname in sim_name.value:
                        y = []
                        for valuename in valuenamecdf_table:
                            y.append(sim_obj[simname][bench_name.value[0]][valuename])           
                        y_plot1[simname] = y
                        plot0.line(valuename_short, y_plot1[simname], legend=simname, line_width=3, line_color=color_index[i])
                        i += 1
                else:
                    plotToAdd = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.append(plotToAdd)

        elif radio_for_vector.active == 2:  # for pdf
            if toggle_plot.active == False:
                plotToRemove = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.remove(plotToRemove)

            if toggle_plot.active == True:
                if not curdoc().get_model_by_name('plot0'): 
                    # make valuename short
                    valuename_short = []
                    count = 0
                    for valuename in valuenamepdf_table:
                        valuename_temp1 = ''
                        for str_t in valuename:
                            if count == 2:
                                valuename_temp1 = valuename_temp1 + str_t
                            if str_t == ':': 
                                count += 1
                        count = 0
                        valuename_short.append(valuename_temp1[:-4]) 

                    plot0 = figure(
                        name='plot0', 
                        title=bench_name.value[0], 
                        x_range=valuename_short, 
                        x_axis_label='value_vector', 
                        y_axis_label='value',
                        width=1600
                    )
                    plot0.xaxis.major_label_orientation='vertical'
                    plotToAdd = plot0
                    y_plot1 = {}
                    i = 0
                    for simname in sim_name.value:
                        y = []
                        for valuename in valuenamecdf_table:
                            y.append(sim_obj[simname][bench_name.value[0]][valuename])           
                        y_plot1[simname] = y
                        plot0.line(valuename_short, y_plot1[simname], legend=simname, line_width=3, line_color=color_index[i])
                        i += 1
                else:
                    plotToAdd = curdoc().get_model_by_name('plot0')
                listOfSubLayouts.append(plotToAdd)

# Set the callback for the toggle button
toggle_plot.on_click(togglePlotCallback)

def toggleTableCallback(attr):
    # Get the layout object added to the documents root
    rootLayout = curdoc().get_model_by_name('mainLayout')
    listOfSubLayouts = rootLayout.children
 
    # Either add or remove the second graph
    if  toggle_table.active == False:
        tableToRemove = curdoc().get_model_by_name('table0')
        listOfSubLayouts.remove(tableToRemove)

    if toggle_table.active == True:
        valuename_table = []
        valuenamecdf_table = []
        valuenamepdf_table = []
        for valuename in value_name_list:
            if re.match(value_name.value+'\S+'+'_cdf', valuename):
                valuenamecdf_table.append(valuename)    
            elif re.match(value_name.value+'\S+'+'_pdf', valuename):
                valuenamepdf_table.append(valuename) 
            elif re.match(value_name.value+'\S+', valuename) or re.match(value_name.value, valuename):
                valuename_table.append(valuename)
        if not curdoc().get_model_by_name('table0'):
            y_plot1 = {}
            if radio_group.active == 0:
                i = 0
                for simname in sim_name.value:
                    y = []
                    for benchname in bench_name.value:
                        y.append(sim_obj[simname][benchname][value_name.value])
                    y_plot1[simname] = y
                    i += 1
                name_str = 'benchname'
                y_plot1[name_str] = bench_name.value
            elif radio_group.active == 1:   # samesim 
                if radio_for_vector.active == 0:  # for value
                    i = 0
                    for benchname in bench_name.value:
                        y = []
                        for valuename in valuename_table:
                            y.append(sim_obj[sim_name.value[0]][benchname][valuename])           
                        y_plot1[benchname] = y
                        i += 1
                    name_str = 'vectorname'
                    y_plot1[name_str] = valuename_table
                if radio_for_vector.active == 1:  # for cdf
                    i = 0
                    for benchname in bench_name.value:
                        y = []
                        for valuename in valuenamecdf_table:
                            y.append(sim_obj[sim_name.value[0]][benchname][valuename])           
                        y_plot1[benchname] = y
                        i += 1
                    name_str = 'vectorname'
                    y_plot1[name_str] = valuenamecdf_table
                if radio_for_vector.active == 2:  # for pdf
                    i = 0
                    for benchname in bench_name.value:
                        y = []
                        for valuename in valuenamepdf_table:
                            y.append(sim_obj[sim_name.value[0]][benchname][valuename])           
                        y_plot1[benchname] = y
                        i += 1
                    name_str = 'vectorname'
                    y_plot1[name_str] = valuenamepdf_table
            elif radio_group.active == 2:   # samebench
                if radio_for_vector.active == 0:  # for value
                    i = 0
                    for simname in sim_name.value:
                        y = []
                        for valuename in valuename_table:
                            y.append(sim_obj[simname][bench_name.value[0]][valuename])           
                        y_plot1[simname] = y
                        i += 1
                    name_str = 'vectorname'
                    y_plot1[name_str] = valuename_table
                if radio_for_vector.active == 1:  # for cdf
                    i = 0
                    for simname in sim_name.value:
                        y = []
                        for valuename in valuenamecdf_table:
                            y.append(sim_obj[simname][bench_name.value[0]][valuename])           
                        y_plot1[simname] = y
                        i += 1
                    name_str = 'vectorname'
                    y_plot1[name_str] = valuenamecdf_table
                if radio_for_vector.active == 2:  # for pdf
                    i = 0
                    for simname in sim_name.value:
                        y = []
                        for valuename in valuenamepdf_table:
                            y.append(sim_obj[simname][bench_name.value[0]][valuename])           
                        y_plot1[simname] = y
                        i += 1
                    name_str = 'vectorname'
                    y_plot1[name_str] = valuenamepdf_table

            table_source = ColumnDataSource(y_plot1)
            columns = []
            columns_name = []
            columns.append(TableColumn(field=name_str, title=name_str))
            columns_name.append(name_str)
            if radio_group.active == 0 or radio_group.active == 2:
                for simname in sim_name.value:
                    columns.append(TableColumn(field=simname, title=simname))
                    columns_name.append(simname)
            elif radio_group.active == 1: # for samesim
                for benchname in bench_name.value:
                    columns.append(TableColumn(field=benchname, title=benchname))
                    columns_name.append(benchname)

            table0 = DataTable(source=table_source, columns=columns, name='table0')
            tableToAdd = table0
        else:
            tableToAdd = curdoc().get_model_by_name('table0')
        listOfSubLayouts.append(tableToAdd)

        if radio_for_csv.active == 0:
            data_list = []
            if radio_group.active == 0:
                for i in range(len(bench_name.value)):
                    data_temp = []
                    for name in columns_name:
                        data_temp.append(y_plot1[name][i])
                    data_list.append(data_temp)
            else:
                if radio_for_vector.active == 0:  # for value
                    for i in range(len(valuename_table)):
                        data_temp = []
                        for name in columns_name:
                            data_temp.append(y_plot1[name][i])
                        data_list.append(data_temp)
                elif radio_for_vector.active == 1:  # for cdf
                    for i in range(len(valuenamecdf_table)):
                        data_temp = []
                        for name in columns_name:
                            data_temp.append(y_plot1[name][i])
                        data_list.append(data_temp)
                if radio_for_vector.active == 0:  # for pdf
                    for i in range(len(valuenamepdf_table)):
                        data_temp = []
                        for name in columns_name:
                            data_temp.append(y_plot1[name][i])
                        data_list.append(data_temp)

            df = pd.DataFrame(data_list, columns=columns_name)
            for_what = ''
            if radio_for_vector.active == 0:  # for value
                for_what = 'forvalue_'
            elif radio_for_vector.active == 1:  # for cdf
                for_what = 'forcdf_'
            elif radio_for_vector.active == 2:  # for pdf
                for_what = 'forpdf_'
            if radio_group.active == 0:
                df.to_csv('./'+'scalar_'+str(value_name.value)+'.csv')
            elif radio_group.active == 1:
                df.to_csv('./'+'vector_samesim_'+for_what+str(value_name.value)+'.csv')
            elif radio_group.active == 2:
                df.to_csv('./'+'vector_samebench_'+for_what+str(value_name.value)+'.csv')
        else:
            print 'Enjoy your life!'

# Set the callback for the toggle button
toggle_table.on_click(toggleTableCallback)

##############################################
input_text = widgetbox(
    sim_name, 
    bench_name, 
    value_name, 
    toggle_plot,
    toggle_table,
)

mainLayout = column(row(input_text, radio_group, radio_for_vector, radio_for_csv), name='mainLayout')
curdoc().add_root(mainLayout)
curdoc().title = "Lines"

