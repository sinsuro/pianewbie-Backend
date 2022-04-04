from scanFile import findStaff
import modules
from pringImg import imgShow
import cv2

if __name__ == '__main__':
    #findStaff('test.jpg')

    # 블로그 코드
    img_0=modules.removeNoise(cv2.imread('test.jpg'))
    img_1,sta=modules.removeLine(img_0)
    img_2,sta=modules.nomalization(img_1,sta,10)
    imgShow("?",img_2)

