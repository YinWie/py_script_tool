import glob
import os

from PIL import Image, ImageFont, ImageDraw
import numpy as np

sample_rate = 0.4  # 抽样率

"""by:音尾"""
def image_change(file):
    im = Image.open(file)  # 读取图片

    font = ImageFont.load_default()
    aspect_ratio = font.getsize("x")[0] / font.getsize("x")[1]
    new_im_size = np.array(
        [im.size[0] * sample_rate, im.size[1] * sample_rate * aspect_ratio]
    ).astype(int)
    im = im.resize(new_im_size)
    im_color = np.array(im)  # 获取原图片颜色
    im = im.convert('L')
    im = np.array(im)  # 图片转换np数组
    symbols = np.array(list(" .-M"))  # 设置输出字符
    if im.max() != im.min():  # 黑屏不执行转换
        im = (im - im.min()) / (im.max() - im.min()) * (symbols.size - 1)
    character = symbols[im.astype(int)]
    lines = "\n".join(("".join(r) for r in character))  # 变量储存字符串结果
    # print(lines) # 打印到控制台
    img_out(font, new_im_size, file, character)  # 图片输出


def img_out(font, new_im_size, file, character):  # 图片输出函数
    letter_size = font.getsize("x")
    im_out_size = new_im_size * letter_size
    bg_color = "black"  # 默认背景颜色黑
    im_out = Image.new("RGB", tuple(im_out_size), bg_color)
    draw = ImageDraw.Draw(im_out)

    y = 0
    for i, line in enumerate(character):
        for j, ch in enumerate(line):
            color = (255, 255, 255)  # 彩色转换注释这行
            # color = tuple(im_color[i, j])  #彩色转换开启这行
            draw.text((letter_size[0] * j, y), ch[0], fill=color, font=font)
        y += letter_size[1]

    if os.path.exists("./out/"):  # 判断是否有输出文件夹
        im_out.save("./out/" + file.split("/")[-1])  # 输出图片
    else:
        os.makedirs("./out/")  # 建立新目录
        im_out.save("./out/" + file.split("/")[-1])  # 输出图片


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
                    image_change(i)
                    print(i + "已输出")
                except:
                    print('程序出错')
        else:
            print("请检查读取文件是否有问题后重新输入")


if __name__ == '__main__':
    main()
