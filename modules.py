# 필요없는 정보 제거
import cv2
import numpy as np
import func as fc
import recognition_modules as rs

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
    line = []  # 오선의 좌표 저장

    for row in range(h):
        pixels = 0
        for col in range(w):
            pixels += (image[row][col] == 255)  # 한 행에 존재하는 흰색 픽셀 개수 셈
        if pixels >= w * 0.5:  # 이미지 넓이의 50%이상 차지
            if len(line) == 0 or abs(line[-1][0] + line[-1][1] - row) > 1:  # 첫 오선이거나 이전에 검출된 오선과 다른오선
                line.append([row, 0])  # 오선 추가 [오선의 y 좌표][오선 높이]
            else:
                line[-1][1] += 1  # 높이 업데이트
    for staff in range(len(line)):
        top_pix = line[staff][0]  # 오선의 최상단 y 좌표
        bot_pix = line[staff][0] + line[staff][1]  # 오선의 최하단 y 좌표
        for col in range(w):
            if image[top_pix - 1][col] == 0 and image[bot_pix + 1][col] == 0:  # 오선 위 아래로 픽셀이 있는지 확인
                for row in range(top_pix, bot_pix + 1):
                    image[row][col] = 0  # 오선지움
    return image, [x[0] for x in line]


# 이미지 정규화
def normalization(img, staves, stdPix):
    avgDis = 0
    lines = int(len(staves) / 5)  # 보표의 개수를 5로 나누면 줄수가 되니까
    for l in range(lines): # 악보 한줄
        for s in range(4): # 보표 한줄
            pos=l*5+s
            avgDis += abs(staves[pos] - staves[pos+1])
    avgDis /= len(staves) - lines  # 평균 간격

    height, wid = img.shape
    weight = stdPix / avgDis

    img = cv2.resize(img, (int(wid * weight),int(height * weight)))
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 이진화
    staves = [x * weight for x in staves]  # 좌표에도 가중치 부여

    return img, staves

def object_detection(image, staves):
    lines = int(len(staves) / 5)  # 보표의 개수
    objects = []  # 구성요소 정보가 저장될 리스트

    closing_image = fc.closing(image)
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        if w >= fc.weighted(5) and h >= fc.weighted(5):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
            center = fc.get_center(y, h)
            for line in range(lines):
                area_top = staves[line * 5] - fc.weighted(20)  # 위치 조건 (상단)
                area_bot = staves[(line + 1) * 5 - 1] + fc.weighted(20)  # 위치 조건 (하단)
                if area_top <= center <= area_bot:
                    objects.append([line, (x, y, w, h, area)])  # 객체 리스트에 보표 번호와 객체의 정보(위치, 크기)를 추가

    objects.sort()  # 보표 번호 → x 좌표 순으로 오름차순 정렬

    return image, objects

def object_analysis(image, objects):
    for obj in objects:
        stats = obj[1]
        stems = fc.stem_detection(image, stats, 30)  # 객체 내의 모든 직선들을 검출함
        direction = None
        if len(stems) > 0:  # 직선이 1개 이상 존재함
            if stems[0][0] - stats[0] >= fc.weighted(5):  # 직선이 나중에 발견되면
                direction = True  # 정 방향 음표
            else:  # 직선이 일찍 발견되면
                direction = False  # 역 방향 음표
        obj.append(stems)  # 객체 리스트에 직선 리스트를 추가
        obj.append(direction)  # 객체 리스트에 음표 방향을 추가

    return image, objects


def recognition(image, staves, objects):
    key = 0
    time_signature = False
    beats = []  # 박자 리스트
    pitches = []  # 음이름 리스트

    for i in range(1, len(objects)):
        obj = objects[i]
        line = obj[0]
        stats = obj[1]
        stems = obj[2]
        direction = obj[3]
        (x, y, w, h, area) = stats
        staff = staves[line * 5: (line + 1) * 5]
        if not time_signature:  # 조표가 완전히 탐색되지 않음 (아직 박자표를 찾지 못함)
            ts, temp_key = rs.recognize_key(image, staff, stats)
            time_signature = ts
            key += temp_key
        else:  # 조표가 완전히 탐색되었음
            pass

        cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)
        fc.put_text(image, i, (x, y - fc.weighted(30)))

    return image, key, beats, pitches