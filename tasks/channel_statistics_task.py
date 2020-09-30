# list.txt にリストされている YouTube チャンネルの動画一覧を取得し保存

import modules.channel_module as channel_module
import settings
import requests
import json


def _fetch_channel_statistics(channel_id: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    payload = {
        "key": settings.API_KEY,
        "part": "statistics",
        "id": channel_id,
    }
    r = requests.get(url, params=payload)
    return r.json()


def _fetch_channel_snippet(channel_id: str):
    url = "https://www.googleapis.com/youtube/v3/channels"
    payload = {
        "key": settings.API_KEY,
        "part": "snippet",
        "id": channel_id,
    }
    r = requests.get(url, params=payload)
    return r.json()


def _build_channel_data(statistics, snippet) -> channel_module.Channel:
    return {
        "id": snippet["items"][0]["id"],
        "name": snippet["items"][0]["snippet"]["title"],
        "published_at": snippet["items"][0]["snippet"]["publishedAt"],
        "view_count": statistics["items"][0]["statistics"]["viewCount"],
        "subscriber_count": statistics["items"][0]["statistics"]["subscriberCount"],
        "video_count": statistics["items"][0]["statistics"]["videoCount"],
        "videos": [],
    }


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
        print(f"Download channel statistics for channel ID: {channel_id} .")
        file_path = f"{settings.OUTPUT_DIR}/{channel_id}.json"
        statistics = _fetch_channel_statistics(channel_id)
        snippet = _fetch_channel_snippet(channel_id)
        _save_to_file(file_path, _build_channel_data(statistics, snippet))


if __name__ == "__main__":
    main()
