import time

from scanFile import findStaff
import modules
from pringImg import imgShow
import cv2
import func as fs
import numpy as np
import os

if __name__ == '__main__':

    # 0-1. 파일 이름 가져오기
    # num=0
    # file_list=os.listdir("data")
    for file_list in os.listdir("data"):
        num = 4
        file_list = os.listdir("data")
        load_file = "data/" + file_list[num]

        # load_file = "data/" + file_list
        # 0-2. 이미지 가져오기
        image_0 = fs.loadImageFromPath(load_file)

        # 1. 보표 영역 추출 및 그 외 노이즈 제거
        image_1 = modules.removeNoise(image_0)

        # 2. 오선 제거
        image_2, staves = modules.removeStaves(image_1)

        standard = 20
        # 3. 악보 이미지 정규화
        image_3, staves = modules.normalization(image_2, staves, standard)

        # 4. 객체 검출 과정
        image_4, objects = modules.object_detection(image_3, staves,standard)

        #4-1. 색반전
        image_4 = 255 - image_4

        #4-2. 노이즈 제거 중
        kernel = np.ones((fs.weighted(2.5), fs.weighted(2.5)), np.uint8)
        image_4_noise = cv2.morphologyEx(image_4, cv2.MORPH_OPEN, kernel)
        # save_file = "data_refine/test1"+fs.saveJpg(file_list[num])
        # save_file = "data_refine/"+fs.saveJpg(file_list)
        # 정규화 악보 이미지 저장
        # cv2.imwrite(filename=save_file,img=image_4_noise)
        # cv2.imwrite(filename=save_file,img=image_4_noise[1400:1800, 2200:3000])

        # cv2.imshow('image', image_4_noise)
        # cv2.imshow('image', image_4_noise[1400:1800, 2200:3000])
        # k = cv2.waitKey(0)
        # if k == 27:
        #     cv2.destroyAllWindows()
        # break



    # # 5. 객체 분석 과정
    # image_5, objects = modules.object_analysis(image_4, objects)
    #
    # # 6. 인식 과정
    # image_6, key, beats, pitches = modules.recognition(image_5, staves, objects)
    #

    # 이미지 띄우기
    # cv2.imshow('image', image_4_noise)
    # k = cv2.waitKey(0)
    # if k == 27:
    #     cv2.destroyAllWindows()




    #
    # findStaff('fireplay.jpg')
    #
    # # 참고용
    # img_0 = modules.removeNoise(cv2.imread('fireplay.jpg'))
    # img_1,sta = modules.removeLine(img_0)
    # # img_2,sta = modules.nomalization(img_1,sta,10)
    #
    # # imgShow("?",img_2)
    #
    #
    # #
    # image_3,sta = modules.nomalization(img_1,sta,10)
    #
    # # image_4, objects = modules.object_detection(image_3, sta)
    #
    # # 이미지 띄우기
    # # cv2.imshow('image', image_4)
    # # k = cv2.waitKey(0)
    # # if k == 27:
    # #     cv2.destroyAllWindows()
    # cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image_3)  # 모든 객체 검출하기
    # for i in range(1, cnt):
    #     (x, y, w, h, area) = stats[i]
    #     cv2.rectangle(image_3, (x, y, w, h), (255, 0, 0), 1)
    #
    # # closing_image = func.closing(image_3)
    # # cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    # # for i in range(1, cnt):
    # #     (x, y, w, h, area) = stats[i]
    # #     cv2.rectangle(image_3, (x, y, w, h), (255, 0, 0), 1)
    # #     func.put_text(image_3, w, (x, y + h + 30))
    # #     func.put_text(image_3, h, (x, y + h + 60))
    # #
    # # closing_image = func.closing(image_3)
    # # cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    # # for i in range(1, cnt):
    # #     (x, y, w, h, area) = stats[i]
    # #     if w >= func.weighted(5) and h >= func.weighted(5):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
    # #         cv2.rectangle(image_3, (x, y, w, h), (255, 0, 0), 1)
    #
    #
    # image_4, objects = modules.object_detection(image_3, sta)

