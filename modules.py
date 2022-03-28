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

def removeLine(image):
    h,w=image.shape
    line=[] # 오선의 좌표 저장

    for row in range(h):
        pixels=0
        for col in range(w):
            pixels+=(image[row][col]==255) # 한 행에 존재하는 흰색 픽셀 개수 셈
        if pixels>=w*0.5: # 이미지 넓이의 50%이상 차지
            if len(line)==0 or abs(line[-1][0]+line[-1][1]-row)>1: #첫 오선이거나 이전에 검출된 오선과 다른오선
                line.append([row,0]) # 오선 추가 [오선의 y 좌표][오선 높이]
            else:
                line[-1][1]+=1 # 높이 업데이트
    for staff in range(len(line)):
        top_pix=line[staff][0] # 오선의 최상단 y 좌표
        bot_pix=line[staff][0]+line[staff][1] # 오선의 최하단 y 좌표
        for col in range(w):
            if image[top_pix-1][col]==0 and image[bot_pix+1][col]==0: # 오선 위 아래로 픽셀이 있는지 확인
                for row in range(top_pix,bot_pix+1):
                    image[row][col]=0 # 오선지움
    return image ,[x[0] for x in line]