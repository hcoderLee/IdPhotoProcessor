# ID Photo Processor

**简介:** 将普通自拍照处理为证件照，先按照1寸照的尺寸等比例裁剪，再填充白色背景。

## 使用

1. 安装依赖：`pip install -r requirements.txt`
2. 打开`id_photo_processor.py`文件，给test_img_path变量赋值，值为要转换照片的路径
3. 运行`python id_photo_processor.py`，在工程内生成**output**目录，其中保存着生成的证件照

## 依赖

本工程使用[PaddleHub](https://paddlehub.readthedocs.io/zh_CN/develop/index.html)中的[deeplabv3p_xception65_humanseg](https://www.paddlepaddle.org.cn/hubdetail?name=deeplabv3p_xception65_humanseg&en_category=ImageSegmentation)模型来识别图片中的人像部分，其作用是将照片中非人像的背景部分变为透明，生成的图片保存在temp目录中

图片的裁剪以及填充背景色是通过[Pillow](https://pillow.readthedocs.io/en/stable/)实现的


