import sys
from PyQt5.QtWidgets import QApplication
from YouTubeMusicApp import YouTubeMusicApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeMusicApp()
    window.resize(1280, 720)
    window.setWindowTitle("YouTube Music App")
    window.show()
    sys.exit(app.exec_())
