import modules.channel_module as channel_module
import settings
import csv
from dateutil.parser import parse


def _convert_date_series_video_view_data(channel_list):

    header = ["Date"]
    data = {}
    for channel_id in channel_list:
        channel_data = channel_module.load_channel_from_file(channel_id)
        header.append(channel_id)
        header.append(f"{channel_id}_title")
        for video in channel_data["videos"]:
            date_obj = parse(video["published_at"])
            date_key = date_obj.strftime("%Y-%m-%d")
            if not date_key in data:
                data[date_key] = {}
            data[date_key][channel_id] = {
                "view": video["view_count"],
                "title": video["title"],
            }

    csv_data = [header]
    for date_key, dic in data.items():
        row = [date_key]
        for channel_id in channel_list:
            view = dic[channel_id]["view"] if channel_id in dic else 0
            row.append(view)
            title = dic[channel_id]["title"] if channel_id in dic else ""
            row.append(title)
        csv_data.append(row)

    file_path = f"{settings.OUTPUT_DIR}/video_view_per_date.csv"
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


def _convert_video_data(channel_list):
    header = [
        "channel_name",
        "video_title",
        "published_at",
        "thumbnail_url",
        "view_count",
        "like_count",
        "dislike_count",
        "favorite_count",
        "comment_count",
    ]

    csv_data = [header]
    for channel_id in channel_list:
        channel_data = channel_module.load_channel_from_file(channel_id)
        for video in channel_data["videos"]:
            row = [
                channel_data["name"],
                video["title"],
                video["published_at"],
                video["thumbnail_url"],
                video["view_count"],
                video["like_count"],
                video["dislike_count"],
                video["favorite_count"],
                video["comment_count"],
            ]
            csv_data.append(row)

    file_path = f"{settings.OUTPUT_DIR}/video.csv"
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


def _convert_channel_data(channel_list):
    header = [
        "name",
        "published_at",
        "view_count",
        "subscriber_count",
        "video_count",
    ]
    csv_data = [header]
    for channel_id in channel_list:
        channel_data = channel_module.load_channel_from_file(channel_id)
        row = [
            channel_data["name"],
            channel_data["published_at"],
            channel_data["view_count"],
            channel_data["subscriber_count"],
            channel_data["video_count"],
        ]
        csv_data.append(row)

    file_path = f"{settings.OUTPUT_DIR}/channel.csv"
    with open(file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)


def main(*args):
    channel_list_file_path = args[0]
    channel_list = channel_module.get_channel_list(channel_list_file_path)
    _convert_channel_data(channel_list)
    _convert_video_data(channel_list)
    _convert_date_series_video_view_data(channel_list)


if __name__ == "__main__":
    main()
