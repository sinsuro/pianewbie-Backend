import cv2
from modules import removeNoise
from pringImg import imgShow
import numpy as np

def findStaff(name):
    img = removeNoise(cv2.imread(name))

    line = []
    width = len(img[0])
    height = len(img)
    start, end = width, 0
    for i in range(height-1):
        line_per = 0
        for j in range(width):
            if img[i][j] == 255:
                line_per += 1
                if start > j:
                    start = j
                if end < j:
                    end = j
        if width * 80 / 100 < line_per and i-1 not in line: # 오선지 두께 및 좌우 간격 고려 추가 필요
            cv2.line(img, [start-20, i], [start-10, i], (255, 255, 255), 1) # 위치 보여주기 위한 테스트 코드
            line.append(i)
    print(line)
    imgShow("test",img)

if __name__ == '__main__':

    findStaff('fireplay.jpg')
