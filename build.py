import os
import shutil
import subprocess


def build_exe():
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

    subprocess.call([
        'pyinstaller', '--onefile', '--windowed', '--name', 'YouTubeMusicApp', 'main.py'
    ])


if __name__ == '__main__':
    build_exe()
