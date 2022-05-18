
import numpy as np
import requests

class Camera():
    def __init__(self, fps=20, video_source=0):
        pass

    def get_frame(self, _bytes=True):
        url = r'http://192.168.0.97/image.jpg'
        resp = requests.get(url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8").tobytes()
        return image

