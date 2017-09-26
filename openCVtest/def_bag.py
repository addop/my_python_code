import cv2


def saveimage(image, showtime, savemode = False):
    # 将图片展示出来, 展示多久和是否保存
    cv2.imshow('image', image)
    print('fig will show ', showtime, ' second')
    k = cv2.waitKey(showtime*1000)
    if savemode == True:
        cv2.imwrite('messigray.png',image)
        print('exported image')
        cv2.destroyAllWindows()
    else:
        cv2.destroyAllWindows()
