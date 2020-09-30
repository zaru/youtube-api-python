from typing import TypedDict

Video = TypedDict(
    "Video",
    {
        "video_id": str,
        "published_at": str,
        "title": str,
        "thumbnail_url": str,
        "view_count": int,
        "like_count": int,
        "dislike_count": int,
        "favorite_count": int,
        "comment_count": int,
    },
)
