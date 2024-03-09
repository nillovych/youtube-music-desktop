from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QPushButton, QLineEdit


def create_button(parent, icon_path, click_action, size=(160, 40), pos=(0, 0)):
    button = QPushButton(parent)
    button.setIcon(QIcon(icon_path))
    button.setIconSize(QtCore.QSize(*size))
    button.move(*pos)
    button.clicked.connect(click_action)
    return button


def create_line_edit(parent, return_action, pos=(200, 20), size=(300, 30)):
    line_edit = QLineEdit(parent)
    line_edit.move(*pos)
    line_edit.resize(*size)
    line_edit.setStyleSheet("background-color: white;")
    line_edit.returnPressed.connect(return_action)
    return line_edit


def create_video_button(parent, video_data, click_action):
    button = QPushButton(f"{video_data['title']} - {video_data['channel']}", parent)
    button.setFont(QFont('Arial', 12))
    button.setStyleSheet("text-align: left; background-color: black; color: white; border: none;")
    button.setIcon(QIcon(video_data['thumbnail']))
    button.setIconSize(QtCore.QSize(30, 30))
    button.clicked.connect(lambda: click_action(video_data))
    return button
