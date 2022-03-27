import cv2
import bitMask as bm
import makeGray as gr
import numpy as np

address = "./test.jpg"

img = cv2.imread(address)
#여기 image를 img로 바꾸고 코드 바꾸면 될 듯?
image=bm.removeNoise(img)

line = []
width = len(img[0])
height = len(img)

cv2.imshow("test",image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# line 찾기
for i in range(height-1):
    linePer = 0
    for j in range(width):
        if img[i][j][2] != 255:
            linePer += 1
    if width * 8 / 10 < linePer:
        cv2.line(img, [100,i], [660,i], (0, 0, 255), 1) # 사진 width로 맞춰야함
        line.append(i)

print(line)
cv2.imshow("test",img)
cv2.waitKey(0)
cv2.destroyAllWindows()