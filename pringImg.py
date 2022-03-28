import cv2

def imgShow(s,img):
    cv2.imshow(s,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()