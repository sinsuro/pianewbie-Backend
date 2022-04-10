import time

from scanFile import findStaff
import modules
from pringImg import imgShow
import cv2
import func

if __name__ == '__main__':
    findStaff('fireplay.jpg')

    # 참고용
    img_0=modules.removeNoise(cv2.imread('fireplay.jpg'))
    img_1,sta = modules.removeLine(img_0)
    # img_2,sta = modules.nomalization(img_1,sta,10)

    # imgShow("?",img_2)


    #
    image_3,sta = modules.nomalization(img_1,sta,10)

    # image_4, objects = modules.object_detection(image_3, sta)

    # 이미지 띄우기
    # cv2.imshow('image', image_4)
    # k = cv2.waitKey(0)
    # if k == 27:
    #     cv2.destroyAllWindows()
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image_3)  # 모든 객체 검출하기
    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        cv2.rectangle(image_3, (x, y, w, h), (255, 0, 0), 1)

    # closing_image = func.closing(image_3)
    # cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    # for i in range(1, cnt):
    #     (x, y, w, h, area) = stats[i]
    #     cv2.rectangle(image_3, (x, y, w, h), (255, 0, 0), 1)
    #     func.put_text(image_3, w, (x, y + h + 30))
    #     func.put_text(image_3, h, (x, y + h + 60))
    #
    # closing_image = func.closing(image_3)
    # cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    # for i in range(1, cnt):
    #     (x, y, w, h, area) = stats[i]
    #     if w >= func.weighted(5) and h >= func.weighted(5):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
    #         cv2.rectangle(image_3, (x, y, w, h), (255, 0, 0), 1)


    image_4, objects = modules.object_detection(image_3, sta)

    imgShow("?",image_4)
    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()
