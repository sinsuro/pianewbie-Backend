import cv2
import numpy as np

def threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image

def findStaff(name):

    img = threshold(cv2.imread(name))
    mask = np.zeros(img.shape, np.uint8)
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(img)
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        if w > img.shape[1] * 0.5:
            cv2.rectangle(mask, (x,y,w,h), (255, 0, 0), -1)
    img = cv2.bitwise_and(img, mask)

    line = []
    width = len(img[0])
    height = len(img)
    start, end = width, 0
    for i in range(height-1):
        linePer = 0
        for j in range(width):
            if img[i][j] == 255:
                linePer += 1
                if start > j:
                    start = j
                if end < j:
                    end = j
        if width * 80 / 100 < linePer and i-1 not in line: # 오선지 두께 및 좌우 간격 고려 추가 필요
            cv2.line(img, [start-20,i], [start-10,i], (255, 255, 255), 1) # 위치 보여주기 위한 테스트 코드
            line.append(i)
    print(line)
    cv2.imshow("test",img)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    findStaff('fireplay.jpg')