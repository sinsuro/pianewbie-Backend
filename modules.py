import cv2
import numpy as np
import func as fc

def removeStaves(image):
    height, width = image.shape
    staves = []  # 오선의 좌표들이 저장될 리스트

    for row in range(height):
        pixels = 0
        for col in range(width):
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 흰색 픽셀의 개수를 셈
        if pixels >= width * 0.5:  # 이미지 넓이의 50% 이상이라면
            if len(staves) == 0 or abs(staves[-1][0] + staves[-1][1] - row) > 1:  # 첫 오선이거나 이전에 검출된 오선과 다른 오선
                staves.append([row, 0])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:  # 이전에 검출된 오선과 같은 오선
                staves[-1][1] += 1  # 높이 업데이트

    for staff in range(len(staves)):
        top_pixel = staves[staff][0]  # 오선의 최상단 y 좌표
        bot_pixel = staves[staff][0] + staves[staff][1]  # 오선의 최하단 y 좌표 (오선의 최상단 y 좌표 + 오선 높이)
        for col in range(width):
            if image[top_pixel - 1][col] == 0 and image[bot_pixel + 1][col] == 0:  # 오선 위, 아래로 픽셀이 있는지 탐색
                for row in range(top_pixel, bot_pixel + 1):
                    image[row][col] = 0  # 오선을 지움

    return image, [x[0] for x in staves]


def removeNoise(image):
    image = fc.preProcessing(image)  # 이미지 이진화
    mask = np.zeros(image.shape, dtype=np.uint8)  # 마스크 생성

    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)  # 레이블링
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > image.shape[1] * 0.5:  # 보표 영역에만
            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1)  # 사각형 그리기

    mask_image = cv2.bitwise_and(image, mask)  # 보표 영약 추출

    return mask_image


def removeLine(image):
    h, w = image.shape
    staves = []  # 오선의 좌표 저장

    for row in range(h):
        pixels = 0
        for col in range(w):
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 흰색 픽셀 개수 셈
        if pixels >= w * 0.5:  # 이미지 넓이의 50%이상 차지
            if len(staves) == 0 or abs(staves[-1][0] + staves[-1][1] - row) > 1:  # 첫 오선이거나 이전에 검출된 오선과 다른오선
                staves.append([row, 0])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:
                staves[-1][1] += 1  # 높이 업데이트
    for staff in range(len(staves)):
        top_pix = staves[staff][0]  # 오선의 최상단 y 좌표
        bot_pix = staves[staff][0] + staves[staff][1]  # 오선의 최하단 y 좌표
        for col in range(w):
            if image[top_pix - 1][col] == 0 and image[bot_pix + 1][col] == 0:  # 오선 위 아래로 픽셀이 있는지 확인
                for row in range(top_pix, bot_pix + 1):
                    image[row][col] = 0  # 오선지움
    return image, [x[0] for x in staves]


# 이미지 정규화
def normalization(image, staves, standard):
    avg_distance = 0
    lines = int(len(staves) / 5)  # 보표의 개수
    for line in range(lines):
        for staff in range(4):
            staff_above = staves[line * 5 + staff]
            staff_below = staves[line * 5 + staff + 1]
            avg_distance += abs(staff_above - staff_below)  # 오선의 간격을 누적해서 더해줌
    avg_distance /= len(staves) - lines  # 오선 간의 평균 간격

    height, width = image.shape  # 이미지의 높이와 넓이
    weight = 3 * standard / avg_distance  # 기준으로 정한 오선 간격을 이용해 가중치를 구함
    new_width = int(width * weight)  # 이미지의 넓이에 가중치를 곱해줌
    new_height = int(height * weight)  # 이미지의 높이에 가중치를 곱해줌
    image = cv2.resize(image, (new_width, new_height), cv2.INTER_LANCZOS4)  # 이미지 리사이징
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 이미지 이진화
    staves = [x * weight for x in staves]  # 오선 좌표에도 가중치를 곱해줌

    return image, staves
