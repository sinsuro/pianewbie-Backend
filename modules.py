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
    weight = standard / avg_distance  # 기준으로 정한 오선 간격을 이용해 가중치를 구함
    new_width = int(width * weight)  # 이미지의 넓이에 가중치를 곱해줌
    new_height = int(height * weight)  # 이미지의 높이에 가중치를 곱해줌

    image = cv2.resize(image, (new_width, new_height))  # 이미지 리사이징
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 이미지 이진화
    staves = [x * weight for x in staves]  # 오선 좌표에도 가중치를 곱해줌

    return image, staves


def object_detection(image, staves,standard):
    lines = int(len(staves) / 5)  # 보표의 개수
    objects = []  # 구성요소 정보가 저장될 리스트

    closing_image = fc.closing(image)
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(closing_image)  # 모든 객체 검출하기
    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        if w >= fc.weighted(standard/2) and h >= fc.weighted(standard/2):  # 악보의 구성요소가 되기 위한 넓이, 높이 조건
            center = fc.get_center(y, h)
            for line in range(lines):
                area_top = staves[line * 5] - fc.weighted(standard*2)  # 위치 조건 (상단)
                area_bot = staves[(line + 1) * 5 - 1] + fc.weighted(standard*2)  # 위치 조건 (하단)
                if area_top <= center <= area_bot:
                    objects.append([line, (x, y, w, h, area)])  # 객체 리스트에 보표 번호와 객체의 정보(위치, 크기)를 추가

    objects.sort()  # 보표 번호 → x 좌표 순으로 오름차순 정렬

    return image, objects


def object_analysis(image, objects):
    for obj in objects:
        # x, y, w, h, area
        stats = obj[1]
        stems = fc.stem_detection(image, stats, 30)  # 객체 내의 모든 직선들을 검출함

        direction = None
        if len(stems) > 0:  # 직선이 1개 이상 존재함
            if stems[0][0] - stats[0] >= fc.weighted(10):  # 직선이 나중에 발견되면
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

    # 수정
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
            # if time_signature:
            #     fc.put_text(image, key, (x, y + h + fc.weighted(20)))
        else:  # 조표가 완전히 탐색되었음
            rs.recognize_note(image, staff, stats, stems, direction)

        cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)
        fc.put_text(image, i, (x, y - fc.weighted(30)))

    return image, key, beats, pitches


# 확인 필요
def recognize_note_head(image, stem, direction):
    (x, y, w, h) = stem
    if direction:  # 정 방향 음표
        area_top = y + h - fc.weighted(7)  # 음표 머리를 탐색할 위치 (상단)
        area_bot = y + h + fc.weighted(7)  # 음표 머리를 탐색할 위치 (하단)
        area_left = x - fc.weighted(14)  # 음표 머리를 탐색할 위치 (좌측)
        area_right = x  # 음표 머리를 탐색할 위치 (우측)
    else:  # 역 방향 음표
        area_top = y - fc.weighted(7)  # 음표 머리를 탐색할 위치 (상단)
        area_bot = y + fc.weighted(7)  # 음표 머리를 탐색할 위치 (하단)
        area_left = x + w  # 음표 머리를 탐색할 위치 (좌측)
        area_right = x + w + fc.weighted(14)  # 음표 머리를 탐색할 위치 (우측)

    cnt = 0  # cnt = 끊기지 않고 이어져 있는 선의 개수를 셈
    cnt_max = 0  # cnt_max = cnt 중 가장 큰 값
    head_center = 0
    pixel_cnt = fc.count_rect_pixels(image, (area_left, area_top, area_right - area_left, area_bot - area_top))

    # get_line, weighted 확인 필 *
    for row in range(area_top, area_bot):
        col, pixels = fc.get_line(image, fc.HORIZONTAL, row, area_left, area_right, 5)
        pixels += 1
        if pixels >= fc.weighted(5):
            cnt += 1
            cnt_max = max(cnt_max, pixels)
            head_center += row

    # 수치 조절 필요 *
    head_exist = (cnt >= 3 and pixel_cnt >= 50)
    head_fill = (cnt >= 6 and cnt_max >= 9 and pixel_cnt >= 60)
    #print(cnt, pixel_cnt, cnt_max)

    # 조건 추가
    if cnt != 0:
        head_center /= cnt

    return head_exist, head_fill, head_center
