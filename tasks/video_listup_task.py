# list.txt にリストされている YouTube チャンネルの動画一覧を取得し保存
# ./output/channels/ に JSON ファイルで動画 ID やタイトル・サムネイル保存している
#
import modules.channel_module as channel_module
import modules.video_module as video_module
import settings
from typing import List
import requests
import json


def _fetch_videos(channel_id: str, page_token: str):
    url = "https://www.googleapis.com/youtube/v3/search"
    payload = {
        "key": settings.API_KEY,
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": "50",
        "order": "date",
        "pageToken": page_token,
    }
    r = requests.get(url, params=payload)
    return r.json()


def _build_video_data(item) -> video_module.Video:
    return {
        "video_id": item["id"]["videoId"],
        "published_at": item["snippet"]["publishedAt"],
        "title": item["snippet"]["title"],
        "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
    }


def _fetch_all_videos_by_channel_id(channel_id: str) -> List[video_module.Video]:
    videos: List[video_module.Video] = []
    page_token = ""
    while True:
        print("*", end="", flush=True)
        json = _fetch_videos(channel_id, page_token)
        if "items" not in json:
            continue
        for item in json["items"]:
            if item["id"]["kind"] != "youtube#video":
                continue
            videos.append(_build_video_data(item))
        if "nextPageToken" in json:
            page_token = json["nextPageToken"]
        else:
            break
    print("")
    return videos


def _save_to_file(file_path: str, data: channel_module.Channel):
    with open(file_path, mode="w") as f:
        text = json.dumps(
            data,
            indent=2,
            ensure_ascii=False,
        )
        f.write(text)


def main(*args):
    channel_list_file_path = args[0]
    channel_list = channel_module.get_channel_list(channel_list_file_path)
    for channel_id in channel_list:
        print(f"Download video list for channel ID: {channel_id} .")
        channel_data = channel_module.load_channel_from_file(channel_id)
        channel_data["videos"] = _fetch_all_videos_by_channel_id(channel_id)
        file_path = f"{settings.OUTPUT_DIR}/{channel_id}.json"
        _save_to_file(file_path, channel_data)


if __name__ == "__main__":
    main()
