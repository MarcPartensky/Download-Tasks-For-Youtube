import hook

videos_filename = "videos.txt"

options = {
    "format": "bestaudio/best",       
    "outtmpl": "%(title)s.%(ext)s",        
    "noplaylist" : True,        
    "progress_hooks": [hook.hook],
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}