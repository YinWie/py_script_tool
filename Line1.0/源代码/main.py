import os
import cv2
import numpy as np
import glob

size = (500, 500)
filter_np = (1, 1)  # 降噪参数
blockSize = 5  # 字体size
C = 2  # 从均值或加权均值提取的常数,越大线稿线越小


def open_img(path):
    image = cv2.imread(path, 0)

    k = np.ones(filter_np, np.uint8)
    img = cv2.morphologyEx(image, cv2.MORPH_OPEN, k, iterations=1)

    img_edge = cv2.adaptiveThreshold(img, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY,
                                     blockSize=blockSize,
                                     C=C)
    img_add = cv2.add(img_edge, img_edge)
    if os.path.exists("./out3/"):  # 判断是否有输出文件夹
        cv2.imwrite("./out3/" + path.split("\\")[-1], img_add)  # 输出图片
    else:
        os.makedirs("./out3/")  # 建立新目录
        cv2.imwrite("./out3/" + path.split("\\")[-1], img_add)  # 输出图片


def main():
    while True:
        print("路径格式案例: ./badapple/*.jpg")
        print("注: *.jpg表示路径下的所有jpg后缀文件")
        print("退出当前脚本请输入: exit")
        file = input("请输入路径:")

        if file == "exit":
            break
        print("输出路径" + "./out/" + "原文件名")
        data = glob.glob(file)  # 读取文件下所有jpg文件
        if data != []:
            for i in data:
                try:
                    open_img(i)
                    print(i + "已输出")
                except:
                    print('程序出错')
        else:
            print("请检查读取文件是否有问题后重新输入")


if __name__ == '__main__':
    main()
