from typing import List, Union, Literal
import modules.channel_module as channel_module
import modules.video_module as video_module
import settings
import requests
import json


def _fetch_video_statistics(video_ids: str):
    url = "https://www.googleapis.com/youtube/v3/videos"
    payload = {
        "key": settings.API_KEY,
        "part": "statistics",
        "id": video_ids,
    }
    r = requests.get(url, params=payload)
    return r.json()


def _save_to_file(file_path: str, data: channel_module.Channel):
    with open(file_path, mode="w") as f:
        text = json.dumps(data, indent=2, ensure_ascii=False)
        f.write(text)


def _chunk_list(list_data: List, chunk=50) -> List[List[str]]:
    return [list_data[i : i + chunk] for i in range(0, len(list_data), chunk)]


def _video_id_list(videos: List[video_module.Video]) -> List[str]:
    return list(map(lambda v: v["video_id"], videos))


def _chunk_video_id_list(videos: channel_module.Channel) -> List[List[str]]:
    video_id_list = _video_id_list(videos["videos"])
    return _chunk_list(video_id_list)


def _find_index(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def _fetch_videos_by_channel_id(channel_id: str) -> Union[List, Literal[False]]:
    channel = channel_module.load_channel_from_file(channel_id)
    if not channel:
        return False

    chunked_video_id_list = _chunk_video_id_list(channel)
    for video_id_list in chunked_video_id_list:
        print("*", end="", flush=True)
        video_statistics = _fetch_video_statistics(",".join(video_id_list))
        if not video_statistics["items"]:
            continue
        for item in video_statistics["items"]:
            video_id = item["id"]
            index = _find_index(channel["videos"], "video_id", video_id)
            channel["videos"][index]["statistics"] = item["statistics"]

    print("")
    return channel["videos"]


def _build_data(item) -> video_module.Video:
    return {
        "video_id": item["video_id"],
        "published_at": item["published_at"],
        "title": item["title"],
        "thumbnail_url": item["thumbnail_url"],
        "view_count": item["statistics"]["viewCount"],
        "like_count": item["statistics"]["likeCount"],
        "dislike_count": item["statistics"]["dislikeCount"],
        "favorite_count": item["statistics"]["favoriteCount"],
        "comment_count": item["statistics"]["commentCount"],
    }


def main(*args):
    channel_list_file_path = args[0]
    channel_list = channel_module.get_channel_list(channel_list_file_path)
    for channel_id in channel_list:
        print(f"Download video statistics for channel ID: {channel_id} .")
        channel_detail = channel_module.load_channel_from_file(channel_id)
        video_list = _fetch_videos_by_channel_id(channel_id)
        if not video_list:
            continue

        videos = list(map(lambda v: _build_data(v), video_list))
        channel_detail["videos"] = videos
        file_path = f"{settings.OUTPUT_DIR}/{channel_id}.json"
        _save_to_file(file_path, channel_detail)


if __name__ == "__main__":
    main()
