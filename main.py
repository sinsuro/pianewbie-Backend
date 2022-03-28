from scanFile import findStaff
import modules
from pringImg import imgShow
import cv2

if __name__ == '__main__':
    #findStaff('test.jpg')

    # 블로그 코드
    img_0=modules.removeNoise(cv2.imread('test.jpg'))
    img_1,line=modules.removeLine(img_0)

    imgShow("?",img_1)

