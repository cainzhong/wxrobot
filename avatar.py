from wxpy import *
import math
import PIL.Image as Image
import os


def save_avatar(group_name=None):
    bot = Bot(cache_path=True)
    if group_name:
        group = ensure_one(bot.groups().search(group_name))
        users = group.members
    else:
        users = bot.friends()

    count = 0
    if not os.path.exists("group-images/"):
        os.mkdir("group-images/")
    for friend in users:
        print(friend.nick_name)
        # 下载头像
        friend.get_avatar("group-images/" + str(count) + ".jpg")
        # 剪成圆形图片
        convert_image_to_circle("group-images/" + str(count) + '.jpg', 'group-images')
        # 删除原图片
        os.remove("group-images/" + str(count) + ".jpg")
        count = count + 1
    # 合并头像
    paste_avatar('group-images')


def convert_image_to_circle(jpgfile, outdir):
    try:
        ima = Image.open(jpgfile).convert("RGBA")
    except:
        return
    size = ima.size

    # 因为是要圆形，所以需要正方形的图片
    r2 = min(size[0], size[1])
    if size[0] != size[1]:
        imb = Image.new('RGBA', (r2, r2), (255, 255, 255, 0))
        pima = ima.load()  # 像素的访问对象
        pimb = imb.load()
        for i in range(r2):
            for j in range(r2):
                pimb[i, j] = pima[(size[0] - r2) / 2 + i, (size[1] - r2) / 2 + j]
    else:
        imb = ima

    # 最后生成圆形图片
    r3 = int(r2 / 2)  # 圆心横坐标 圆的半径
    imc = Image.new('RGBA', (r3 * 2, r3 * 2), (0, 0, 0, 0))
    pimb = imb.load()  # 像素的访问对象
    pimc = imc.load()

    for i in range(r2):
        for j in range(r2):
            lx = abs(i - r3)  # 到圆心距离的横坐标
            ly = abs(j - r3)  # 到圆心距离的纵坐标
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径

            if l < r3:
                pimc[i, j] = pimb[i, j]
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # os.path.splitext()用于将文件名与扩展名分离，否则图片仍然会保存为jpg格式，从而报错
    imc.save(os.path.join(outdir, os.path.basename(os.path.splitext(jpgfile)[0]) + '.png'))


def paste_avatar(avatar_dir):
    # 获取下载的头像文件
    ls = os.listdir(avatar_dir)

    # 排序
    ls.sort(key=lambda x: int(x[:-4]))

    # 头像墙尺寸
    image = Image.open('bg.png')
    image_size = image.size[0]
    # image_size = 2560

    each_size = math.floor(image_size / math.ceil(math.sqrt(len(ls))))
    y_lines = x_lines = math.ceil(math.sqrt(len(ls)))
    # image = Image.new('RGBA', (each_size * x_lines, each_size * y_lines), (0, 0, 0, 0))

    x = 0
    y = 0

    for file_names in ls:
        try:
            img = Image.open("group-images/" + file_names)
            print("正在处理" + file_names.split('.png')[0] + "/" + str(len(ls)))
        except IOError:
            continue
        else:
            img = img.resize((each_size, each_size))
            # 粘贴png
            image.paste(img, (x * each_size, y * each_size), img.split()[3])
            x += 1
            if x == x_lines:
                x = 0
                y += 1

    img = image.save("all.png")


def arrangeImagesInCircle(masterImage, imagesToArrange):
    master_image = Image.open(masterImage)
    imgWidth, imgHeight = master_image.size
    # we want the circle to be as large as possible.
    # but the circle shouldn't extend all the way to the edge of the image.
    # If we do that, then when we paste images onto the circle, those images will partially fall over the edge.
    # so we reduce the diameter of the circle by the width/height of the widest/tallest image.
    diameter = 120
    radius = diameter / 2
    circleCenterX = imgWidth / 2
    circleCenterY = imgHeight / 2
    theta = 2 * math.pi / len(imagesToArrange)
    for i in range(len(imagesToArrange)):
        curImg = Image.open('group-images/'+imagesToArrange[i])
        curImg = curImg.resize((50, 50))
        angle = i * theta
        dx = int(radius * math.cos(angle))
        dy = int(radius * math.sin(angle))
        # dx and dy give the coordinates of where the center of our images would go.
        # so we must subtract half the height/width of the image to find where their top-left corners should be.
        pos = (
            int(circleCenterX + dx - curImg.size[0] / 2),
            int(circleCenterY + dy - curImg.size[1] / 2)
        )
        print(pos)
        master_image.paste(curImg, pos, curImg.split()[3])
    master_image.save("new.png")


if __name__ == '__main__':
    # save_avatar('Python新手交流蓝群')
    # paste_avatar('group-images')
    ls = os.listdir('group-images')
    ls.sort(key=lambda x: int(x[:-4]))
    arrangeImagesInCircle('bg.png', ls)

# 获取文件所在的绝对路径
# def get_dir(sys_arg):
#     sys_arg = sys_arg.split("/")
#     dir_str = ""
#     count = 0
#     for cur_dir in sys_arg:
#         if count == 0:
#             count = count + 1
#         if count == len(sys_arg):
#             break
#         dir_str = dir_str + cur_dir + "/"
#         count = count + 1
#     return dir_str
#
#
# curr_dir = get_dir(sys.argv[0])
# bot = Bot()
#
# # 机器人账号自身
# myself = bot.self
# my_friends = bot.friends(update=True)
#
# if not os.path.exists(curr_dir + "group-images/"):
#     os.mkdir(curr_dir + "group-images/")
#
# count = 0
# for friend in my_friends:
#     print(friend.nick_name)
#     friend.get_avatar(curr_dir + "group-images/" + str(count) + ".jpg")
#     count = count + 1
#
# # 获取下载的头像文件
# ls = os.listdir(curr_dir + 'group-images')
#
# # 去除非 .jpg 文件
# for filter_ls in ls:
#     if ".jpg" in filter_ls:
#         continue
#     else:
#         ls.remove(filter_ls)
#
# # 排序
# ls.sort(key=lambda x: int(x[:-4]))
#
# # 头像墙尺寸
# image_size = 2560
#
# each_size = math.floor(image_size / math.floor(math.sqrt(len(ls))))
# x_lines = math.ceil(math.sqrt(len(ls)))
# y_lines = math.ceil(math.sqrt(len(ls)))
# image = Image.new('RGB', (each_size * x_lines, each_size * y_lines))
#
# x = 0
# y = 0
#
# for file_names in ls:
#     try:
#         img = Image.open(curr_dir + "group-images/" + file_names)
#         print("正在处理" + file_names.split('.jpg')[0] + "/" + str(len(ls)))
#     except IOError:
#         continue
#     else:
#         img = img.resize((each_size, each_size))
#         image.paste(img, (x * each_size, y * each_size))
#         x += 1
#         if x == x_lines:
#             x = 0
#             y += 1
#
# img = image.save(curr_dir + "all.jpg")
#
# try:
#     shutil.rmtree(curr_dir + "group-images/")
#     print("收尾，清理临时文件")
# except FileNotFoundError:
#     print("没什么好删的")
#
# print("！！！\n生成完毕了，放在了目录" + curr_dir + "，去看看吧。")
