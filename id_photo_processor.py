import os
import paddlehub as hub
from PIL import Image

# 待预测图片
test_img_path = ''
# 保存生成的人像抠图，背景透明
hunmanseg_output_dir = './temp/'
# 保存最终生成的白底证件照
output_dir = './output/'


# 分离人像，背景透明，生成图片保存在 ./humanseg_output/
def split_humanseg(path):
    module = hub.Module(name="deeplabv3p_xception65_humanseg")

    output = hunmanseg_output_dir + get_img_name(path) + '.png'
    # 如果要生成的图片已存在，则删除
    if os.path.exists(output):
        os.remove(output)

    # execute predict and print the result
    results = module.segmentation(paths=[path], visualization=True, output_dir=hunmanseg_output_dir)
    for result in results:
        print("save human seg image at: %s" % result["save_path"])


# 填充白色背景
def inflate_bg(img_name):
    im = Image.open(hunmanseg_output_dir + img_name + '.png')
    # (alpha band as paste mask).
    p = Image.new('RGBA', im.size, (250, 250, 250))
    p.paste(im, mask=im)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_path = output_dir + img_name + '.png'
    p.save(output_path)
    resize_2_1inch(output_path)


# 获取图片文件名（无后缀）
def get_img_name(path):
    return os.path.basename(path).split('.')[0]


# 裁剪并缩放原始图片为一寸
def resize_2_1inch(path):
    im = Image.open(path)
    WIDTH_1IN = 295
    HEIGHT_1IN = 413
    # 按1寸照的比例裁剪图片
    width, height = im.size
    rate = height / width
    if rate < (HEIGHT_1IN / WIDTH_1IN):
        x = (width - int(height / HEIGHT_1IN * WIDTH_1IN)) / 2
        im = im.crop((x, 0, x + (int(height / HEIGHT_1IN * WIDTH_1IN)), height))
    else:
        y = (height - int(width / WIDTH_1IN * HEIGHT_1IN)) / 2
        im = im.crop((0, y, width, y + (int(width / WIDTH_1IN * HEIGHT_1IN))))

    # 缩放图片为1寸大小
    im = im.resize((WIDTH_1IN, HEIGHT_1IN))
    im.save(path)


if __name__ == '__main__':
    if not os.path.exists(test_img_path):
        print("image %s not exist!" % test_img_path)
        exit(1)

    split_humanseg(test_img_path)
    inflate_bg(get_img_name(test_img_path))
    # resize_2_1inch(test_img_path)
