# 이진화 및 다크모드
import cv2
import numpy as np

def preProcessing(img):
    img=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret,img=cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    return img

def put_text(image, text, loc):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, str(text), loc, font, 0.6, (255, 0, 0), 2)

def weighted(value):
    standard = 10
    return int(value * (standard / 10))

def closing(image):
    kernel = np.ones((weighted(5), weighted(5)), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

def get_center(y, h):
    return (y + y + h) / 2

