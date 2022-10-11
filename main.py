import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow,QWidget,QSizePolicy,QPushButton,QLineEdit,QApplication,QVBoxLayout,QInputDialog,QLabel,QComboBox,QRadioButton,QHBoxLayout,QGroupBox,QCheckBox, QStyleFactory, QVBoxLayout, QScrollArea, QSlider
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from PyQt5 import sip
import time
from win32api import GetSystemMetrics
import math

#API
from pprint import pprint
from Google import Create_Service

#Player
import pafy
import vlc

from PIL import Image
import requests


CLIENT_SECRET_FILE = 'client-secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']


service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

instance = vlc.Instance()
player = instance.media_player_new()



#font_id = font_ttf.addApplicationFont("font.ttf")
#print(font_id)
#families = QFontDatabase().applicationFontFamilies(font_id)
#font = QFont(families[0])


class Window(QtWidgets.QWidget):    
    def __init__(self):

        super().__init__()
        self.setStyleSheet("background-color: black;")

        self.main_win()

    def sign_in(self):
        def click(objects):
            CLIENT_SECRET_FILE = {
                "installed": {"client_id": "714470650373-7coibpe2ibsq7tanad5ocimgei8oqg4n.apps.googleusercontent.com",
                              "project_id": "youtube-data-329111", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                              "token_uri": "https://oauth2.googleapis.com/token",
                              "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                              "client_secret": "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",
                              "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]}}
            API_NAME = 'youtube'
            API_VERSION = 'v3'
            SCOPES = ['https://www.googleapis.com/auth/youtube']
            global service

            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


            #self.clear(objects)

        self.log_but = QtWidgets.QPushButton(self)
        self.log_but.setIcon(QIcon('login_but.png'))
        self.log_but.setIconSize(QtCore.QSize(300, 150))
        self.log_but.move(500,250)
        self.log_but.clicked.connect(click)
        self.log_but.show()
        objects = []
        objects.append(self.main_win)



    def clear(self, objects):
        for i in range(len(objects)):
            objects[i].deleteLater()
        self.main_win()


    def main_win(self):
        print('hi')
        objects = []
        global check_play
        check_play = 1

        self.main_but = QtWidgets.QPushButton(self)
        self.main_but.setIcon(QIcon('main_but.png'))
        self.main_but.setIconSize(QtCore.QSize(160, 40))
        self.main_but.move(-30,10)
        self.main_but.clicked.connect(lambda: self.clear(objects))
        objects.append(self.main_but)
        self.main_but.show()

        self.line = QLineEdit(self)
        self.line.move(200, 20)
        self.line.resize(300, 30)
        #self.line.textChanged.connect(text)
        self.line.setStyleSheet("background-color: white;")
        self.line.returnPressed.connect(lambda: self.search(objects))
        self.line.show()
        objects.append(self.line)

        a = self.you_liked()



        def half_pos(a):
            for i in range(len(objects)):
                objects[i].deleteLater()

            objects_hp = []

            self.line = QLineEdit(self)
            self.line.move(200, 20)
            self.line.resize(300, 30)
            # self.line.textChanged.connect(text)
            self.line.setStyleSheet("background-color: white;")
            self.line.returnPressed.connect(lambda: self.search(objects_hp))
            self.line.show()
            objects_hp.append(self.line)

            self.main_but = QtWidgets.QPushButton(self)
            self.main_but.setIcon(QIcon("main_but.png"))
            self.main_but.setIconSize(QtCore.QSize(160, 40))
            self.main_but.move(-30, 10)
            self.main_but.clicked.connect(lambda: self.clear(objects_hp))
            self.main_but.show()


            self.layout = QVBoxLayout()

            #self.layout.deleteLater()
            #objects_hp.append(self.layout)

            f = 50
            j = 0
            for i in range(0, len(a), 4):
                f = f + 40

                resp = requests.get(a[i+2])
                file = open(f'images/list/{a[i+3]+a[i]}.png', 'wb')
                file.write(resp.content)
                file.close()

                im = Image.open(f'images/list/{a[i+3]+a[i]}.png')
                im = im.crop((105, 45, 370, 320))
                im.save(f'images/list/{a[i+3]+a[i]}.png')

                self.pf = QtWidgets.QPushButton('   '+a[i]+'\n'+'   '+a[i+3],self)
                self.pf.setFont(QFont('EuclidFlex-Light', 12))
                self.pf.setStyleSheet("QPushButton{text-align: left;background-color: black; color: white; border-style: outset; border-width: 0px; border-color: rgb(36,36,36);};QPushButton:pressed{background-color:rgb(36,36,36)}")
                self.pf.setIcon(QIcon(f'images/list/{a[i+3]+a[i]}.png'))
                self.pf.setIconSize(QtCore.QSize(30, 30))


                self.pf.clicked.connect(lambda ch, b=a[i+1], c=a[i+2], d=a[i], f=a[i+3], obj =[], objects_hp = objects_hp: self.play(b,c,d,f,objects_hp,obj))

                #self.pf.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                self.layout.addWidget(self.pf, j)
                #self.layout.addWidget(self.lable, j+1)
                j+=1

            self.w = QWidget()
            self.w.setParent(self)
            self.w.setLayout(self.layout)


            self.mw = QScrollArea()
            self.mw.setStyleSheet("QScrollBar {background: black;}QScrollBar:vertical {border: none;width: 10px;}QScrollBar:horizontal {border: none;width: 0px;}QScrollBar::handle:vertical{background: rgb(36,36,36)}")
            self.mw.setParent(self)
            self.mw.setWidget(self.w)
            self.mw.resize(500, 550)
            self.mw.move(750,100)
            self.mw.show()
            objects_hp.append(self.mw)

            self.label_f = QLabel(self)
            self.label_f.setGeometry(750, 100, 2, 550)
            self.label_f.setStyleSheet("background-color: black")
            self.label_f.show()
            objects_hp.append(self.label_f)

            self.label_g = QLabel(self)
            self.label_g.setGeometry(1249,100,2, 550)
            self.label_g.setStyleSheet("background-color:black")
            self.label_g.show()
            objects_hp.append(self.label_g)

            self.label_h = QLabel(self)
            self.label_h.setGeometry(750, 100, 500,2)
            self.label_h.setStyleSheet("background-color:black")
            self.label_h.show()
            objects_hp.append(self.label_h)

            self.label_j = QLabel(self)
            self.label_j.setGeometry(750,648,500,2)
            self.label_j.setStyleSheet("background-color:black")
            self.label_j.show()
            objects_hp.append(self.label_j)

        self.ul = QtWidgets.QPushButton(self)
        self.ul.setIcon(QIcon("images/youliked.png"))
        self.ul.setIconSize(QtCore.QSize(200, 200))
        self.ul.move(50,145)
        you_mas = self.you_liked()
        self.ul.clicked.connect(lambda: half_pos(you_mas))
        self.ul.show()
        objects.append(self.ul)

        all_lists = self.all_lists()
        a = 50
        r = 1
        for i in range(0, len(all_lists), 3):
            aflor = self.all_lists_items()

            if aflor[i] != []:
                resp = requests.get(all_lists[i + 2])
                file = open(f'images/list_{all_lists[i]}.png', 'wb')
                file.write(resp.content)
                file.close()

                self.playlist = QtWidgets.QPushButton(self)
                self.playlist.setIcon(QIcon(f'images/list_{all_lists[i]}.png'))
                self.playlist.setIconSize(QtCore.QSize(320, 240))
                self.playlist.move(a + 350, 120)
                self.playlist.clicked.connect(lambda ch, items_mass = aflor[i]: half_pos(items_mass))
                self.playlist.show()
                r+=1

                objects.append(self.playlist)

                a += 360
                self.title = QLabel(self)
                self.title.setFont(QFont('Arial', 12))
                self.title.setGeometry(a, 360, 200, 30)
                self.title.setText(all_lists[i]+':')
                self.title.setStyleSheet("color: white")
                objects.append(self.title)
                self.title.show()

        self.label_3 = QLabel(self)
        self.label_3.setFont(QFont('Arial', 12))
        self.label_3.setGeometry(60, 360, 200, 30)
        self.label_3.setText("Songs you liked:")
        self.label_3.setStyleSheet("color: white")
        self.label_3.show()
        objects.append(self.label_3)

        self.label_2 = QLabel(self)
        self.label_2.setFont(QFont('Arial', 16))
        self.label_2.setGeometry(50, 100, 200, 30)
        self.label_2.setText("Your Playlists:")
        self.label_2.setStyleSheet("color: white")
        self.label_2.show()
        objects.append(self.label_2)
        print('bie')
        
    def play(self, id, thumb, name_song, name_singer, obj, obj_srch):
        self.main_but.deleteLater()



        self.main_but = QtWidgets.QPushButton(self)
        self.main_but.setIcon(QIcon("main_but.png"))
        self.main_but.setIconSize(QtCore.QSize(160, 40))
        self.main_but.move(-30, 10)

        if obj == []:
            obj = obj_srch
            aloki = 1
            for i in range(len(obj_srch)):
                obj_srch[i].deleteLater()
        else:
            aloki = 7
        self.main_but.clicked.connect(lambda: self.clear(obj))
        self.main_but.show()
        if len(obj) > aloki:
            obj.pop(-1)


        self.line = QLineEdit(self)
        self.line.move(200, 20)
        self.line.resize(300, 30)
        #self.line.textChanged.connect(text)
        self.line.setStyleSheet("background-color: white;")
        self.line.returnPressed.connect(lambda: self.search(obj))
        self.line.show()
        obj.append(self.line)

        def pause_func():
            player.pause()
            check = self.but.text()
            if check == '':
                self.but.setIcon(QIcon('play.png'))
                self.but.setText('`')
            if check == '`':
                self.but.setIcon(QIcon('pause.png'))
                self.but.setText('')

        def changed_vol(value):
            player.audio_set_volume(value*5)

        def create_vol():
            self.slider1.setValue(int(player.audio_get_volume()/5))
            self.slider1.show()

        def changed_slider(value):
            #player.audio_set_volume(0)
            end_point = int(player.get_length() / 1000)
            pos = value/end_point
            player.set_position(pos)
            #def sl_rel():
                #player.audio_set_volume(100)
            #self.slider.sliderReleased(sl_rel)

        def media_time_changed(event):
            #global end_time
            end_point = int(player.get_length() / 1000)
            #if media_t == 0:
            self.slider.setMaximum(end_point)
            def funnic(a):
                if a/10 < 1:
                    a = f'0{a}'
                return a
            #print(player.get_position())
            falin = int(player.get_position()*end_point)
            #print(f'pos = {player.get_position()}, len = {end_point}, falin = {falin}')
            self.slider.setValue(falin)

            time = player.get_time()
            time_show = int(time/1000)

            time_min = math.floor(time_show/60)
            time_sec = time_show - (time_min*60)
            end_time_minutes = math.floor(end_point/60)
            end_time_seconds = end_point - (end_time_minutes*60)

            time_min = funnic(time_min)
            time_sec = funnic(time_sec)
            end_time_minutes = funnic(end_time_minutes)
            end_time_seconds = funnic(end_time_seconds)

            self.label_time.setText(f'{time_min}:{time_sec} / {end_time_minutes}:{end_time_seconds}')
        global check_play
        if check_play == 0 :
           check_mass = [self.label_1, self.but, self.but1, self.but2, self.ul, self.slider]
           for i in range(len(check_mass)):
               sip.delete(check_mass[i])


        self.ul = QtWidgets.QPushButton(self)
        self.ul.setIcon(QIcon(f"images/list/{name_singer+name_song}.png"))
        self.ul.setIconSize(QtCore.QSize(600, 400))
        self.ul.move(0,150)
        self.ul.show()
        self.ul.clicked.connect(pause_func)
        obj.append(self.ul)

        self.label_1 = QLabel(self)
        self.label_1.setGeometry(0, int(653*height/900), int(width*0.8), int(150*height/1600))
        self.label_1.setStyleSheet("background-color: rgb(36,36,36)")
        self.label_1.show()


        self.label_time = QLabel(self)
        self.label_time.setGeometry(160, 672, 200, 30)
        self.label_time.setStyleSheet("background-color: rgba(255, 255, 255, 0); color: white")
        self.label_time.show()


        self.but = QtWidgets.QPushButton(self)
        self.but.setText('')
        self.but.setIcon(QIcon('play.png'))
        self.but.setIconSize(QtCore.QSize(35, 35))
        self.but.move(60,667)
        self.but.clicked.connect(pause_func)
        self.but.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.but.show()


        self.vol = QtWidgets.QPushButton(self)
        self.vol.setIcon(QIcon('volume.png'))
        self.vol.setIconSize(QtCore.QSize(35, 35))
        self.vol.move(1200,667)
        self.vol.clicked.connect(create_vol)
        self.vol.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.vol.show()

        self.but1 = QtWidgets.QPushButton(self)
        self.but1.setIcon(QIcon('nt.png'))
        self.but1.setIconSize(QtCore.QSize(25, 25))
        self.but1.move(110,672)
        self.but1.clicked.connect(lambda: self.nexttrack(id,thumb))
        self.but1.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.but1.show()

        self.but2 = QtWidgets.QPushButton(self)
        self.but2.setIcon(QIcon('pt.png'))
        self.but2.setIconSize(QtCore.QSize(25, 25))
        self.but2.move(15,672)
        self.but2.clicked.connect(lambda: self.prevtrack(id,thumb))
        self.but2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.but2.show()


        
        player.stop()
        
        url = 'https://www.youtube.com/watch?v='+id
        video = pafy.new(url)
        best = video.getbestaudio()
        playurl = best.url

        media = instance.media_new(playurl)
        media.get_mrl()

        
        player.set_media(media)
        

        self.but.setIcon(QIcon('pause.png'))
        player.play()

        #media_t = 0

        self.vlc_event_manager = player.event_manager()
        self.vlc_event_manager.event_attach(vlc.EventType.MediaPlayerTimeChanged, media_time_changed)

        #media_t = 1

        self.slider1 = QSlider(self)
        self.slider1.setOrientation(QtCore.Qt.Horizontal)
        self.slider1.setTickPosition(QSlider.TicksBelow)
        self.slider1.setTickInterval(1)
        self.slider1.setMinimum(0)
        self.slider1.setMaximum(20)
        self.slider1.setGeometry(1095, 685, 100, 3)
        #self.slider1.setStyleSheet("QSlider {min-height: 10px;}QSlider::groove:horizontal {border: 0px; background: black;height: 20px;border-radius: 0px;}QSlider::handle {background: black;height: 20px;width: 20px;border-radius: 10px;}QSlider::sub-page:horizontal {background: #FF0000;border-top-left-radius: 0px;border-bottom-left-radius: 0px;}QRangeSlider {qproperty-barColor: #FF0000;}")
        self.slider1.setStyleSheet("QSlider::handle {background: white;height: 10px;width: 10px;border-radius: 10px;}QSlider::sub-page:horizontal {background: white;border-top-left-radius: 0px;border-bottom-left-radius: 0px;}QRangeSlider {qproperty-barColor: white;}")
        self.slider1.valueChanged.connect(changed_vol)


        self.slider = QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.setMinimum(0)
        #self.slider.setMaximum(end_point)
        self.slider.setGeometry(0, 650, 1280, 3)
        self.slider.sliderMoved.connect(changed_slider)
        self.slider.setStyleSheet("QSlider::handle {background: red;height: 10px;width: 10px;border-radius: 10px;}QSlider::sub-page:horizontal {background: #FF0000;border-top-left-radius: 0px;border-bottom-left-radius: 0px;}QRangeSlider {qproperty-barColor: #FF0000;}")
        self.slider.show()

        check_play = 0



        self.label_song = QLabel(self)
        self.label_song.setFont(QFont('EuclidFlex-Light', 10))
        self.label_song.setGeometry(570, 680, 200, 30)
        self.label_song.setText(name_singer)
        self.label_song.setStyleSheet("background-color: rgba(255, 255, 255, 0);color: white")
        self.label_song.show()

        self.label_name = QLabel(self)
        self.label_name.setFont(QFont('EuclidFlex-Light', 10))
        self.label_name.setGeometry(570, 665, 200, 30)
        self.label_name.setText(name_song)
        self.label_name.setStyleSheet("background-color: rgba(255, 255, 255, 0);color: white")
        self.label_name.show()

        self.logo = QtWidgets.QPushButton(self)
        self.logo.setIcon(QIcon(f"images/list/{name_singer+name_song}.png"))
        self.logo.setIconSize(QtCore.QSize(50, 50))
        self.logo.move(500, 660)
        self.logo.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.logo.show()
        


    def signin(self):
        part_string = 'contentDetails,statistics,snippet'
        video_ids = 'v2AC41dglnM'

        response = service.videos().list(
            part=part_string,
            id=video_ids
        ).execute()

        pprint(response)
        
    def search(self, objects):
        objects_hp = []
        a = str(self.line.text())

        self.layout = QVBoxLayout()

        self.line = QLineEdit(self)
        self.line.move(200, 20)
        self.line.resize(300, 30)
        #self.line.textChanged.connect(text)
        self.line.setStyleSheet("background-color: white;")
        self.line.returnPressed.connect(lambda: self.search(objects))
        self.line.show()
        objects_hp.append(self.line)

        for i in range(len(objects)):
            objects[i].deleteLater()
        self.main_but = QtWidgets.QPushButton(self)
        self.main_but.setIcon(QIcon("main_but.png"))
        self.main_but.setIconSize(QtCore.QSize(160, 40))
        self.main_but.move(-30, 10)
        self.main_but.clicked.connect(lambda: self.clear(objects_hp))
        self.main_but.show()
        self.w = QWidget()
        self.w.setParent(self)
        self.w.setLayout(self.layout)




        artist_info = []
        artist_exist = a + ' - Topic'
        responce_chn = service.search().list(part='snippet', q=artist_exist, type='channel', maxResults = 1).execute()
        if responce_chn.get('items') != []:
            snip = responce_chn.get('items')[0].get('snippet')

            image_chn = snip.get('thumbnails').get('medium').get('url')
            name_chn = snip.get('title').replace(' - Topic', '')


            self.label_3 = QLabel(self)
            self.label_3.setFont(QFont('Arial', 16))
            self.label_3.setGeometry(620, 200, 200, 30)
            self.label_3.setText(name_chn)
            self.label_3.setStyleSheet("color: white")
            self.label_3.show()
            objects_hp.append(self.label_3)

            response_ph = requests.get(image_chn)
            file = open("images/chn_pht.png", "wb")
            file.write(response_ph.content)
            file.close()

            self.ph_chn = QtWidgets.QPushButton(self)
            self.ph_chn.setIcon(QIcon("images/chn_pht.png"))
            self.ph_chn.setIconSize(QtCore.QSize(70,70))
            self.ph_chn.move(450, 250)
            self.ph_chn.show()
            objects_hp.append(self.ph_chn)


            artist_info.extend((snip.get('title').replace(' - Topic', ''), snip.get('channelId'), snip.get('thumbnails').get('medium').get('url')))
            songs_artist = service.search().list(part='snippet', channelId = artist_info[1], type = 'video').execute().get('items')
            #lists_artist = service.search().list(part='snippet', channelId=artist_info[1], type='playlist').execute()
            for i in range(len(songs_artist)):
                id = songs_artist[i].get('id').get('videoId')
                thumb = songs_artist[i].get('snippet').get('thumbnails').get('high').get('url')
                name_song = songs_artist[i].get('snippet').get('title')
                name_singer = artist_info[0]

                self.pf = QtWidgets.QPushButton(name_singer+' - '+name_song, self)
                self.pf.setStyleSheet("background-color: rgb(36,36,36);color:white")
                self.pf.setFont(QFont('Arial', 15))
                self.pf.clicked.connect(lambda ch, id = id, thum = thumb, name_song = name_song, name_singer = name_singer, obj=[], objects_hp= objects_hp: self.play(id, thumb, name_song, name_singer, obj, objects_hp))


                self.layout.addWidget(self.pf, i)
        self.w.move(600,300)
        self.w.show()
        objects_hp.append(self.w)

                 


            #for i in range(len(songs_artist.get('items'))):
            #pprint(songs_artist.get('items'))
            #playlists_artist = service.playlists().list(part = 'snippet', channelId = artist_info[1]).execute()
        #print(artist_info)
        responce_vids = service.search().list(part='snippet', q=a, type='video', maxResults = 5).execute()
        #pprint(responce_vids)


        #self.signin(id_bb)


    def all_lists(self):
        all_playlists = service.playlists().list(mine = True, part='id, snippet').execute()
        a = []
        for i in range(len(all_playlists.get('items'))):
            id = all_playlists.get('items')[i].get('id')
            pic = all_playlists.get('items')[i].get('snippet').get('thumbnails').get('high').get('url')
            title = all_playlists.get('items')[i].get('snippet').get('title')
            a.extend((title,id,pic))
        return a

    def all_lists_items(self):
        lists_info = self.all_lists()
        all_lists_parsed = []
        for i in range(0, len(lists_info), 3):
            fabun = service.playlistItems().list(part = 'snippet', playlistId=lists_info[i+1], maxResults = 50).execute()

            npt = fabun.get('nextPageToken')
            check = fabun.get('items')
            list = []
            for j in range(len(check)):

                id = check[j].get('snippet').get('resourceId').get('videoId')
                video = service.videos().list(part = 'snippet', id = id).execute()
                check_4_mus = video.get('items')
                #pprint(check_4_mus)
                if check_4_mus != []:

                    category = check_4_mus[0].get('snippet').get('categoryId')
                    if category == '10':
                        name_of_singer = check_4_mus[0].get('snippet').get('channelTitle')
                        name_of_singer_pars = name_of_singer.replace(' - Topic', '')

                        list.extend((check_4_mus[0].get('snippet').get('title'), check_4_mus[0].get('id'),
                                     check_4_mus[0].get('snippet').get('thumbnails').get('high').get('url'), name_of_singer_pars))
            all_lists_parsed.append(list)
            all_lists_parsed.extend(([], []))
        return all_lists_parsed




    def you_liked(self):

        #print('Videos you liked:')
        a = []

        liked = service.videos().list(part = 'snippet', myRating='like', maxResults = 50).execute()
        npt = liked.get('nextPageToken')
        check = liked.get('items')


        for i in range(len(check)):
            check_f = check[i].get('snippet').get('categoryId')
            if check_f == '10':
                name_of_singer = check[i].get('snippet').get('channelTitle')
                name_of_singer_pars = name_of_singer.replace(' - Topic', '')
                a.extend((check[i].get('snippet').get('title'), check[i].get('id'), check[i].get('snippet').get('thumbnails').get('high').get('url'), name_of_singer_pars))
        total = int(liked.get('pageInfo').get('totalResults'))
        total = total-50
        
        while total > 0:
        
            liked_np = service.videos().list(part = 'snippet', myRating='like', maxResults = 50, pageToken=npt).execute()
            npt = liked_np.get('nextPageToken')

            check = liked_np.get('items')
            for i in range(len(check)):
                check_f = check[i].get('snippet').get('categoryId')
                if check_f == '10':
                    name_of_singer = check[i].get('snippet').get('channelTitle')
                    name_of_singer_pars = name_of_singer.replace(' - Topic', '')
                    #print(name_of_singer_pars)
                    a.extend((check[i].get('snippet').get('title'), check[i].get('id'), check[i].get('snippet').get('thumbnails').get('high').get('url'), name_of_singer_pars))
            total = total-50


        return(a)

        #a = all_playlists.get('items')
        #c = []
        #for i in range(len(a)):
            #b1 = a[i].get('id')
            #b2 = a[i].get('snippet').get('title')
            #c.extend([b2,b1])

        #print(c)
        #pprint(responce)
            
        #responce1 = service.playlistItems().list(playlistId = c[n], part='snippet',maxResults = 50, fields='pageInfo, items/snippet(title, description)').execute()
        #pprint(responce1)
        #self.signin(id_bb)
        
        

if __name__ == '__main__':
    app1 = QtWidgets.QApplication(sys.argv)
    app_icon = QIcon()
    app_icon.addFile('logo.ico')
    app1.setWindowIcon(app_icon)
    #app1.setStyle('Breeze')
    window = Window()
    #if width >= 1000:
    window.resize(1280,720)
    #elif width < 1000:
        #window.resize(int(height*0.75),int(height*0.9))
    #window.setStyleSheet("background-color: black;")
    window.setWindowTitle("Youtube Music App")
    window.show()
    sys.exit(app1.exec())
