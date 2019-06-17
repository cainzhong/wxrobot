# -*- coding: utf-8 -*-
__author__ = 'www.outofmemory.cn'
import math
from PIL import Image


def arrangeImagesInCircle(masterImage, imagesToArrange):
    imgWidth, imgHeight = masterImage.size

    # we want the circle to be as large as possible.
    # but the circle shouldn't extend all the way to the edge of the image.
    # If we do that, then when we paste images onto the circle, those images will partially fall over the edge.
    # so we reduce the diameter of the circle by the width/height of the widest/tallest image.
    diameter = min(
        imgWidth - max(img.size[0] for img in imagesToArrange),
        imgHeight - max(img.size[1] for img in imagesToArrange)
    )
    radius = diameter / 2

    circleCenterX = imgWidth / 2
    circleCenterY = imgHeight / 2
    theta = 2 * math.pi / len(imagesToArrange)
    for i in range(len(imagesToArrange)):
        curImg = imagesToArrange[i]
        angle = i * theta
        dx = int(radius * math.cos(angle))
        dy = int(radius * math.sin(angle))

        # dx and dy give the coordinates of where the center of our images would go.
        # so we must subtract half the height/width of the image to find where their top-left corners should be.
        pos = (
            int(circleCenterX + dx - curImg.size[0] / 2),
            int(circleCenterY + dy - curImg.size[1] / 2)
        )
        masterImage.paste(curImg, pos)


img = Image.new("RGB", (500, 500), (255, 255, 255))

# 下面的三个图片是3个 50x50 的pngs 图片，使用了绝对路径，需要自己进行替换成你的图片路径
imageFilenames = ["group-images/1.png", "group-images/2.png",
                  "group-images/3.png"] * 5
images = [Image.open(filename) for filename in imageFilenames]

arrangeImagesInCircle(img, images)

img.save("output.png")
