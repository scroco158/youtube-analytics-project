import json
import isodate
from googleapiclient.discovery import build
import os
from datetime import timedelta


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, play_list_id):

        self.play_list_id = play_list_id  # id плейлиста

        # получаем список видео плейлиста по его play_list_id
        self.video_list = self.youtube.playlistItems().list(playlistId=self.play_list_id,
                                                            part='id,snippet,contentDetails',
                                                            maxResults=50).execute()
        with open('video_list.json', 'w') as f:
            json.dump(self.video_list, f, indent=4, ensure_ascii=False)

        # получаем channel_id из данных по первому видео
        self.channel_id = self.video_list['items'][0]['snippet']['channelId']

        # получаем список плейлистов этого канала
        self.play_lists_list = self.youtube.playlists().list(channelId=self.channel_id,
                                                             part='contentDetails,snippet',
                                                             maxResults=50).execute()

        # ищем в этом списке по play_list_id название этого плейлиста
        for item in self.play_lists_list['items']:
            if play_list_id == item['id']:
                self.title = item['snippet']['title']
                break

        # сохраним id всех видео нашего плейлиста в список
        self.video_id_list = []
        for item in self.video_list['items']:
            self.video_id_list.append(item['contentDetails']['videoId'])

        self.url = 'https://www.youtube.com/playlist?list=' + self.play_list_id

        self.__total_duration = self.__total_duration()

    @property
    def total_duration(self):
        return self.__total_duration

    def __total_duration(self):

        """
        Возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)
        """

        total_time = timedelta()
        for item in self.video_id_list:
            total_time += self.get_time_video(item)
        return total_time

    def get_time_video(self, vi_id):
        """
        Возвращает продолжительность видео по его id
        """
        # получение данных по видео
        time_data = self.youtube.videos().list(part='snippet,contentDetails,statistics ',
                                               id=vi_id,
                                               maxResults=50).execute()

        # получаем продолжительность из json в формате ("duration": "PT6M54S")
        # это iso_8601 работать для работы с ним модуль isodate

        duration_in_iso = time_data['items'][0]['contentDetails']['duration']
        duration_in_datetime = isodate.parse_duration(time_data['items'][0]['contentDetails']['duration'])

        # print(duration_in_iso)
        # print(duration_in_datetime)
        # print(type(duration_in_iso))
        # print(type(duration_in_datetime))

        return duration_in_datetime

    def show_best_video(self):
        # буду использовать self.video_id_list создается при инициализации и содержит
        # id всех видео плейлиста
        #
        # сделаем словарь {'id плейлиста': количество лайков по этому видео}
        #
        likes_dict = {}
        for item in self.video_id_list:
            likes_data = self.youtube.videos().list(part='snippet,contentDetails,statistics ',
                                                    id=item,
                                                    maxResults=50).execute()
            likes_dict[item] = int(likes_data['items'][0]['statistics']['likeCount'])

        # сортируем словарь по убыванию количества лайков
        likes_dict_sorted = sorted(likes_dict.items(), key=lambda para: para[1], reverse=True)

        # получаем ссылочку на видео с макс. кол-вом лайков
        best_video_url = 'https://youtu.be/' + likes_dict_sorted[0][0]

        return best_video_url

