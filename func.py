# 이진화 및 다크모드
import cv2
import numpy as np

VERTICAL = True
HORIZONTAL = False

def preProcessing(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

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

def get_line(image, axis, axis_value, start, end, length):
    if axis:
        points = [(i, axis_value) for i in range(start, end)]  # 수직 탐색
    else:
        points = [(axis_value, i) for i in range(start, end)]  # 수평 탐색
    pixels = 0
    for i in range(len(points)):
        (y, x) = points[i]
        pixels += (image[y][x] == 255)  # 흰색 픽셀의 개수를 셈
        next_point = image[y + 1][x] if axis else image[y][x + 1]  # 다음 탐색할 지점
        if next_point == 0 or i == len(points) - 1:  # 선이 끊기거나 마지막 탐색임
            if pixels >= weighted(length):
                break  # 찾는 길이의 직선을 찾았으므로 탐색을 중지함
            else:
                pixels = 0  # 찾는 길이에 도달하기 전에 선이 끊김 (남은 범위 다시 탐색)
    return y if axis else x, pixels


#여기일지도?
def stem_detection(image, stats, length):
    (x, y, w, h, area) = stats
    stems = []  # 기둥 정보 (x, y, w, h)
    for col in range(x, x + w):
        end, pixels = get_line(image, VERTICAL, col, y, y + h, length)
        if pixels:
            if len(stems) == 0 or abs(stems[-1][0] + stems[-1][2] - col) >= 1:
                (x, y, w, h) = col, end - pixels + 1, 1, pixels
                stems.append([x, y, w, h])
            else:
                stems[-1][2] += 1
    #print(stems)
    return stems

def count_rect_pixels(image, rect):
    x, y, w, h = rect
    pixels = 0
    for row in range(y, y + h):
        for col in range(x, x + w):
            if image[row][col] == 255:
                pixels += 1
    return pixels

def loadImageFromPath(imgPath):
    try:
        # gif 처리
        if str(imgPath).lower().endswith('.gif'):
            gif = cv2.VideoCapture(imgPath)
            ret, frame = gif.read()  # ret=True if it finds a frame else False.
            if ret:
                return frame
        else:
            return cv2.imread(imgPath)
    except Exception as e:
        print(e)
        return None

def saveJpg(imgPath):
    saveImgPath,ext=imgPath.split(".")
    saveImgPath+=".jpg"

    return saveImgPath