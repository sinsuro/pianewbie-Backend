# 필요없는 정보 제거
import cv2
import numpy as np
import makeGray as gr

def removeNoise(image):
    image=gr.preProcessing(image) # 이미지 이진화
    mask = np.zeros(image.shape, dtype=np.uint8)  # 마스크 생성

    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > image.shape[1] * 0.5: # 보표 영역에만
            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1) # 사각형 그리기

    mask_image = cv2.bitwise_and(image, mask) # 보표 영약 추출

    return mask_image