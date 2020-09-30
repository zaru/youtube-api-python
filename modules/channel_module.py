from typing import List, TypedDict
import modules.video_module as video_module
import settings
import os
import json

Channel = TypedDict(
    "Channel",
    {
        "id": str,
        "name": str,
        "published_at": str,
        "view_count": int,
        "subscriber_count": int,
        "video_count": int,
        "videos": List[video_module.Video],
    },
)


def get_channel_list(file_path) -> List[str]:
    with open(file_path) as f:
        channel_list = f.read().split("\n")
    return list(filter(None, channel_list))


def load_channel_from_file(channel_id: str) -> Channel:
    file_path = f"{settings.OUTPUT_DIR}/{channel_id}.json"
    if not os.path.exists(file_path):
        raise Exception(f"File does not exists. {file_path}")
    with open(file_path) as f:
        return json.load(f)


def load_channel_from_file_to_str(channel_id: str) -> str:
    file_path = f"{settings.OUTPUT_DIR}/{channel_id}.json"
    if not os.path.exists(file_path):
        raise Exception(f"File does not exists. {file_path}")
    with open(file_path) as f:
        return f.read()
