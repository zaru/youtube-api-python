from bokeh.io import save, output_file
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
import itertools
import pandas as pd
import modules.channel_module as channel_module

channel_list_file_path = "./list.txt"
channel_list = channel_module.get_channel_list(channel_list_file_path)

output_file("plot.html")
df = pd.read_csv("./output/video_view_per_date.csv", index_col="Date", parse_dates=True)
df = df.sort_values(by=["Date"], ascending=True)
source = ColumnDataSource(df)
plot = figure(
    plot_width=1200,
    plot_height=600,
    x_axis_label="Date",
    y_axis_label="View",
    x_axis_type="datetime",
)
colors = itertools.cycle(palette)
for channel_id, color in zip(channel_list, colors):
    channel_data = channel_module.load_channel_from_file(channel_id)
    print(channel_data["id"])
    plot.line(
        x="Date",
        y=channel_data["id"],
        source=source,
        color=color,
        line_width=2,
        legend_label=channel_data["name"],
        name=channel_data["id"],
    )
    hover = HoverTool(
        tooltips=[
            ("View", f"@{channel_data['id']}"),
            ("Title", f"@{channel_data['id']}_title"),
        ],
        names=[channel_data["id"]],
    )
    plot.add_tools(hover)

plot.yaxis[0].formatter = NumeralTickFormatter(format="0")
save(plot)
