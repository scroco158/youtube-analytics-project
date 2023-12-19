import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.id = self.channel['items'][0]['id']                               # id канала
        self.title = self.channel['items'][0]['snippet']['title']               # название канала
        self.description = self.channel['items'][0]['snippet']['description']  # - описание канала
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']  # - ссылка на канал
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']    # - количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']    # - количество видео
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']    # - общее количество просмотров

    def __str__(self):
        """Название и ссылку на канал по шаблону < название_канала > (< ссылка_на_канал >)"""
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __eg__(self, other):
        return self.subscriberCount == other.subscriberCount

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, file_name):
        channel_info = {'id': self.id, 'title': self.title, 'description': self.description,
                        'url': self.url, 'subscriberCount': self.subscriberCount, 'video_count': self.video_count,
                        'viewCount': self.viewCount}

        with open(file_name, 'w',) as file:
            json.dump(channel_info, file, indent=4)
