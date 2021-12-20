import cv2 as cv

# 调用摄像头
cap = cv.VideoCapture(0)

num = 1

while (cap.isOpened()):
    ret_flag, Vshow = cap.read()
    cv.imshow('Capture_Test', Vshow)
    k = cv.waitKey(1) & 0xFF
    if k == ord('s'):  # 保存
        cv.imwrite('img/' + str(num) + '.myface' + '.jpg', Vshow)
        print('success to save' + str(num) + '.jpg')
        print('-----------------------')
        num += 1
    if face:



# 释放内存
cv.destroyAllWindows()
# 释放摄像头
cap.release()
