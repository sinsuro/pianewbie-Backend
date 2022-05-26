import cv2
import numpy as np

def template_matching(img,template):
    # 입력이미지와 템플릿 이미지 읽기
    template= cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    th, tw = template.shape[:2]
    cv2.imshow('template', template)

    # 3가지 매칭 메서드 순회
    methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF_NORMED']
    for i, method_name in enumerate(methods):
        img_draw = img.copy()
        method = eval(method_name)
        # 템플릿 매칭   ---①
        res = cv2.matchTemplate(img, template, method)
        # 최솟값, 최댓값과 그 좌표 구하기 ---②
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(method_name, min_val, max_val, min_loc, max_loc)

        # TM_SQDIFF의 경우 최솟값이 좋은 매칭, 나머지는 그 반대 ---③
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
            match_val = min_val
        else:
            top_left = max_loc
            match_val = max_val
        # 매칭 좌표 구해서 사각형 표시   ---④
        bottom_right = (top_left[0] + tw, top_left[1] + th)
        cv2.rectangle(img_draw, top_left, bottom_right, (255, 0, 0), 2)
        # 매칭 포인트 표시 ---⑤
        cv2.putText(img_draw, str(match_val), top_left, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow(method_name, img_draw)
    cv2.waitKey(0)
    cv2.destroyAllWindows()