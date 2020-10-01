from bokeh.io import save, output_file
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox
import pandas as pd
import modules.channel_module as channel_module

channel_list_file_path = "./list.txt"
channel_list = channel_module.get_channel_list(channel_list_file_path)

output_file("make_table_posting_interval.html")
df = pd.read_csv("./output/posting_interval.csv")
source = ColumnDataSource(df)

columns = [
    TableColumn(field="Channel", title="Channel"),
    TableColumn(field="ViewCount", title="ViewCount"),
    TableColumn(field="SubscriberCount", title="SubscriberCount"),
    TableColumn(field="VideCount", title="VideCount"),
    TableColumn(field="PostingInterval", title="PostingInterval"),
]

data_table = DataTable(
    source=source, columns=columns, fit_columns=True, width=1300, height=800
)
save(widgetbox([data_table], sizing_mode="scale_both"))
