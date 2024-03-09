from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QScrollArea

from services.youtube_service import YouTubeService
from ui_components import create_button, create_line_edit, create_video_button
from services.vlc_player import VLCPlayer

class YouTubeMusicApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: black;")
        self.youtube_service = YouTubeService()
        self.vlc_player = VLCPlayer()
        self.main_window()

    def main_window(self):
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.main_button = create_button(self, 'main_but.png', self.clear_objects)
        self.search_line = create_line_edit(self, self.search)
        self.setup_layout()

    def setup_layout(self):
        self.main_button.show()
        self.search_line.show()

    def clear_objects(self):
        for widget in self.findChildren(QtWidgets.QWidget):
            widget.deleteLater()
        self.setup_ui()

    def search(self):
        search_query = self.search_line.text()
        self.clear_objects()
        self.search_line = create_line_edit(self, self.search)
        self.search_line.setText(search_query)
        self.search_line.show()

        search_results = self.youtube_service.get_search_results(search_query)

        layout = QVBoxLayout()
        for result in search_results:
            video_button = create_video_button(self, result, self.play_video)
            layout.addWidget(video_button)

        container = QtWidgets.QWidget()
        container.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollBar {background: black;} QScrollBar:vertical {border: none;width: 10px;} QScrollBar::handle:vertical {background: rgb(36,36,36);}")

        scroll_area.resize(500, 550)
        scroll_area.move(750, 100)
        scroll_area.show()

    def play_video(self, video_data):
        self.vlc_player.play(video_data['video_id'])
