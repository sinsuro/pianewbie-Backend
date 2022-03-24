import cv2
address = "./test.jpg"
img = cv2.imread(address)
cv2.imshow("test",img)
cv2.waitKey()
cv2.destroyAllWindows()
