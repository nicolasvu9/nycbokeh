from bokeh.layouts import row, column, widgetbox
from bokeh.plotting import figure, show, output_file, ColumnDataSource
from bokeh.models.widgets import Select
from bokeh.models import SingleIntervalTicker
from bokeh.io import curdoc, show
from bokeh.layouts import row
import pandas as pd
from pathlib import Path
import os, sys

parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
nyc_grouped_file_path = os.path.join(parentdir,'data', 'nyc_grouped.csv')
nyc_avg_file_path = os.path.join(parentdir,'data', 'nyc_avg.csv')

df=pd.read_csv(nyc_grouped_file_path)
df2=pd.read_csv(nyc_avg_file_path)
zips=df.columns.tolist()
zip_code= '00083'


def get_data(zip_code):
    dictionary = {}
    dictionary['month']=list(df.loc[:,'month'])
    dictionary['average_hours_zip']=list(df.loc[:,zip_code])
    return dictionary


source= ColumnDataSource(data=get_data(zip_code))
source2= ColumnDataSource(data=get_data(zip_code))

p = figure( title = 'NYC Monthly avg response time to complaints by zipcode', plot_height = 350, plot_width = 800)
p.xgrid.grid_line_color = None
p.ygrid.grid_line_alpha = 0.5
p.xaxis.axis_label = 'month'
p.yaxis.axis_label = 'average hours'

r = p.line(x = 'month', y = 'average_hours_zip',source = source, line_color = 'navy', legend = "ZIPCODE 1")
r2 = p.line(x = 'month', y = 'average_hours_zip',source = source2, line_color = 'red', legend = "ZIPCODE 2")
r3 = p.line(x=df2['month'], y=df2['diff_hours'], line_color= 'black', legend = "Total average")


select = Select(title='zipcode 1', options=zips[1:], value=zip_code)
select2 = Select(title='zipcode 2', options=zips[1:], value=zip_code)


def update_zip(attrname, old, new):
    source.data = get_data(select.value)

def update_zip2(attrname, old, new):
    source2.data = get_data(select2.value)


select.on_change('value', update_zip)
select2.on_change('value', update_zip2)

p.legend.location = 'top_left'
p.legend.title = 'ZIP CODES'
p.legend.title_text_font = 'Arial'
p.legend.title_text_font_size = '10pt'
p.xaxis.ticker = SingleIntervalTicker(interval=1)

curdoc().add_root(column(select, select2, p))