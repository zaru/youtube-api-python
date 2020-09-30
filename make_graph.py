import pandas_bokeh
from bokeh.io import save, output_file
from bokeh.models import ColumnDataSource, NumeralTickFormatter, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
import itertools
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import settings
import json
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

# plot.line(
#     x="Date",
#     y="mu",
#     source=source,
#     line_color="red",
#     line_width=2,
#     legend_label="ムーザル",
#     name="lines1",
# )
# plot.line(
#     x="Date",
#     y="pi",
#     source=source,
#     line_color="blue",
#     line_width=2,
#     legend_label="競合 A",
#     name="lines2",
# )
# plot.yaxis[0].formatter = NumeralTickFormatter(format="0")
# hover1 = HoverTool(
#     tooltips=[("View", "@mu"), ("Title", "@mu_title")],
#     names=["lines1"],
# )
# plot.add_tools(hover1)
# hover2 = HoverTool(
#     tooltips=[("View", "@pi"), ("Title", "@pi_title")],
#     names=["lines2"],
# )
# plot.add_tools(hover2)


# df = pd.read_csv("./output/video.csv")
# plt.figure()
# for key, grp in df.groupby("channel_name"):
#     plt.plot(grp["published_at"], grp["view_count"], label=key)
# # df.plot(x="published_at", y="view_count")
# plt.savefig("graph.png")
# plt.close("all")
# print("graph.png")

# channel = channel_module.load_channel_from_file("UCLPHXwLp90A5R69Eltxo-sg")
# if channel == False:
#     exit()
#
# df = pd.DataFrame(
#     {
#         "Date": list(map(lambda v: v["published_at"], channel["videos"])),
#         "View": list(map(lambda v: int(v["view_count"]), channel["videos"])),
#     }
# )
# df["Date"] = pd.to_datetime(df["Date"])
# df.set_index("Date", inplace=True)
# # df = df.set_index("Date")
#
# # json_str = json.dump(channel)
# # print(channel)
# # df_f = pd.read_json(f"{settings.OUTPUT_DIR}/UCLPHXwLp90A5R69Eltxo-sg.txt")
# #
# #
# plt.figure()
# # plt.scatter(df.index, df["View"])
#
# df.plot()
# # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
# # plt.show()
# plt.savefig("pandas_iris_line.png")
# plt.close("all")

# date_index = pd.date_range("2020-01-25", periods=10, freq="D")
# print(date_index)
