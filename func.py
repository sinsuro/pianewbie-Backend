import cv2

def preProcessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    return img

def loadImageFromPath(imgPath):
    return cv2.imread(imgPath)


