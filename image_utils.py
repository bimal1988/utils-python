import cv2
import PIL
import numpy as np


def cv2pil(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    return image


def pil2cv(image):
    image = np.array(image)
    image = image[:, :, ::-1]
    return image
