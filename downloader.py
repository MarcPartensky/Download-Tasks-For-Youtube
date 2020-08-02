import youtube_dl as ytdl
import json
import os


class VideoTasksDownloader:
    """Manage task of downloading videos when possible."""
    def __init__(self,
        options:dict,
        videos_filename:str="videos.txt",
        videos_folder:str="videos",
    ):
        """Uses the filename of the list of videos."""
        self.options = options
        self.videos_filename = videos_filename
        self.videos_folder = videos_folder

    @property
    def videos(self):
        """Get the list of videos."""
        with open(self.videos_filename, 'r') as file:
            video_list = file.read()
        if video_list=="":
            return []
        return video_list.split('\n')

    @videos.setter
    def videos(self, video_list:list):
        """Set the list of videos to another."""
        with open(self.videos_filename, 'w') as file:
            file.write('\n'.join(video_list))

    @videos.deleter
    def videos(self):
        """Clear the list of videos."""
        with open(self.videos_filename, 'w'):
            pass
        
    @property
    def parsed_videos(self):
        """Return the videos parsed for youtube-dl format before downloading.
        Indeed youtube-dl only accepts urls by default. To download videos (or musics)
        based on their title it's necessary to add 'ytsearch:[video name]'."""
        videos = []
        for video in self.videos:
            if not video.startswith('http'):
                video = f"ytsearch:{video}"
            videos.append(video)
        return videos

    def download(self):
        """Try to download the videos with youtube-dl."""
        parsed_videos = self.parsed_videos
        options = self.options
        current_working_directory = os.getcwd()
        os.chdir(self.videos_folder)
        with ytdl.YoutubeDL(options) as downloader:
            downloader.download(parsed_videos)
        os.chdir(current_working_directory)
        del self.videos

    def download_terminal(self):
        """Try to download the videos with youtube-dl by using commands."""
        while len(self.videos) > 0:
            video = self.videos[0]
            cmd = [
                    'youtube-dl',
                    '-ciw',
                    '-x',
                    '--audio-format',
                    'mp3',
                    '--audio-quality',
                    '0',
                    '-f',
                    'bestaudio'
                    '--embed-thumbnail',
                    '-o',
                    "'%(title    )s.%(ext)s'",
                    '--rm-cache-dir',
                    video
                ]
            cmd = ' '.join(cmd)
            os.system(cmd)
            self.videos = self.videos[1:]

    def clear_videos_folder(self):
        """Remove all cache and stuff in videos folder."""
        for file in os.listdir(self.videos_folder):
            pass
            # if file.endswith('.mp3') or file.endswith('.mp4'):
            #     pass





