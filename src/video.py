import os
from googleapiclient.discovery import build
import json
from src.channel import Channel

class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_video):
        self.id_video = id_video  # id видео
        self.request = self.youtube.videos().list(part="snippet,statistics", id=self.id_video)
        self.response = self.request.execute()
        self.name = self.response['items'][0]['snippet']['title']  # название видео
        self.view_count = self.response['items'][0]['statistics']['viewCount']  # просмотры
        self.like_count = self.response['items'][0]['statistics']['likeCount']  # лайки
        self.url = f'https://www.youtube.com/watch?v={self.id_video}'

        #print(self.url)
        # print(self.response)
        # with open('video_data.json', 'w') as f:
        #     json.dump(self.response, f, indent=4, ensure_ascii=False)

    def __str__(self):
        return self.name


class PLVideo(Video):

    def __init__(self, vid_id, pl_id):
        super().__init__(vid_id)
        self.pl_id = pl_id
