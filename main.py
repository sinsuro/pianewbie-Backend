import time

import modules
import cv2
import func as fs
import os

if __name__ == '__main__':

    fname = 0
    for file_list in os.listdir("data"):

        if str(file_list).lower().endswith('.gif'):
            continue

        fname += 1
        load_file = "data/" + file_list

        # 0-2. 이미지 가져오기
        image_0 = fs.loadImageFromPath(load_file)

        # 1. 보표 영역 추출 및 그 외 노이즈 제거
        image_1 = modules.removeNoise(image_0)

        # 2. 오선 제거
        image_2, staves = modules.removeStaves(image_1)

        standard = 20
        # 3. 악보 이미지 정규화
        image_3, staves = modules.normalization(image_2, staves, standard)

        #3-1. 색반전
        image_3 = 255 - image_3

        cv2.imshow('test', image_3)
        k = cv2.waitKey(0)
        if k == 27:
            cv2.destroyAllWindows()
        time.sleep(10000)

        # #4-2. 노이즈 제거 중
        # kernel = np.ones((fs.weighted(2.5), fs.weighted(2.5)), np.uint8)
        # image_4_noise = cv2.morphologyEx(image_4, cv2.MORPH_OPEN, kernel)

        print(len(staves))
        for i in range(len(staves)//5):
            save_file = "data_seg_refine/" + str(fname) + "_" + str(i+1) + ".jpg"
            print(save_file, "완료")
            cv2.imwrite(filename=save_file, img=image_3[int(staves[i*5]-300):int(staves[i*5+4]+300),100:-100])