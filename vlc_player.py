import vlc


class VLCPlayer:
    def __init__(self):
        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

    def play(self, video_id):
        url = f'https://www.youtube.com/watch?v={video_id}'
        video = pafy.new(url)
        best = video.getbestaudio()
        playurl = best.url
        media = self.vlc_instance.media_new(playurl)
        self.player.set_media(media)
        self.player.play()
