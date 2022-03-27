import cv2
import numpy as np

address = "./test.jpg"
img = cv2.imread(address)
line = []
width = len(img[0])
height = len(img)
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
cv2.waitKey()
cv2.destroyAllWindows()