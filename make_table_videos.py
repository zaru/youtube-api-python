from bokeh.io import save, output_file
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox
import pandas as pd
import modules.channel_module as channel_module

channel_list_file_path = "./list.txt"
channel_list = channel_module.get_channel_list(channel_list_file_path)

output_file("make_table_videos.html")
df = pd.read_csv("./output/video.csv")
df["like_ratio"] = df["like_count"] / df["view_count"] * 100
df["comment_ratio"] = df["comment_count"] / df["view_count"] * 100
df = df.round({"like_ratio": 2, "comment_ratio": 2})
source = ColumnDataSource(df)

columns = [
    TableColumn(field="channel_name", title="channel_name"),
    TableColumn(field="video_title", title="video_title"),
    TableColumn(field="view_count", title="view_count"),
    TableColumn(field="like_count", title="like_count"),
    TableColumn(field="like_ratio", title="like_ratio"),
    TableColumn(field="dislike_count", title="dislike_count"),
    TableColumn(field="comment_count", title="comment_count"),
    TableColumn(field="comment_ratio", title="comment_ratio"),
]

data_table = DataTable(
    source=source, columns=columns, fit_columns=True, width=1300, height=800
)
save(widgetbox([data_table], sizing_mode="scale_both"))
