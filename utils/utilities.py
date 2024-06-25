import requests
from PIL import Image


def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

    img = Image.open(save_path)
    img = img.crop((105, 45, 370, 320))
    img.save(save_path)
