import os
from googleapiclient.discovery import build
import json


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, id_video):
        self.id_video = id_video
        self.request = self.youtube.videos().list(part="snippet,contentDetails", id=self.id_video)
        self.response = self.request.execute()
        #print(self.response)
        self.name = self.response['items'][0]['snippet']['title']
        # print(self.name)
        # print(self.response)

        # with open('video_data.json', 'w') as f:
        #     json.dump(self.response, f, indent=4, ensure_ascii=False)

    def __str__(self):
        return self.name


class PLVideo:
    pass
