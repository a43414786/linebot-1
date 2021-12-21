import cv2


import numpy as np
import cv2

size1 = (2500,843)
size2 = (2500,1686)

img = np.zeros((843,1250, 3), np.uint8)
img2 = np.zeros((843,1250, 3), np.uint8)
img.fill(255)
img = np.concatenate((img,img2), axis=1)
print(img.shape)
cv2.imwrite("test.jpg", img)
cv2.imshow('My Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


img = np.zeros((400, 400, 3), np.uint8)

def test(img):
    # 文字
    text = 'Hello, OpenCV!'

    # 使用各種字體
    cv2.putText(img, text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 80), cv2.FONT_HERSHEY_PLAIN,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 120), cv2.FONT_HERSHEY_DUPLEX,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 160), cv2.FONT_HERSHEY_COMPLEX,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 200), cv2.FONT_HERSHEY_TRIPLEX,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 240), cv2.FONT_HERSHEY_COMPLEX_SMALL,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 280), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.putText(img, text, (10, 320), cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
    1, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow('My Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
test(img)