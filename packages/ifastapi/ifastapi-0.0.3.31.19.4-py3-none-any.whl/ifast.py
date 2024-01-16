import glob
import os
import shutil
import sys
import uuid
import zipfile
from PIL import Image, ImageFilter, ImageDraw, ImageFont


def main():
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case 'init':
                copy_file()
            case 'code_pic':
                if len(sys.argv) < 3:
                    raise "参数不足,需要转换图片的文件名称及转换图片大小"
                dir_name = sys.argv[2]
                size = (300, 150)
                if len(sys.argv) > 3:
                    size = tuple(map(int, sys.argv[3].split(',')))
                compress_pic(dir_name, dir_name, size)


def copy_file():
    # 拷贝文件到运行目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    zip_directory = os.path.dirname(current_directory)
    zip_directory = os.path.dirname(zip_directory)
    # 要复制的目录名称
    zip_file_name = 'init_builder.zip'
    destination_dir = os.getcwd()

    # 压缩包文件路径
    zip_file_path = os.path.join(zip_directory, zip_file_name)

    # 打开压缩包
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # 解压所有文件到目标目录
        zip_ref.extractall(destination_dir)


def compress_pic(path, save_path, size=(300, 150)):
    """
    压缩图片
    将文件夹里的图片压缩为验证码图片规格大小 300x150
    """
    jpg_list = glob.glob(f'{path}/*.jpg')
    for i, jpg in enumerate(jpg_list):
        jpg_path = os.path.join('.', jpg)
        im = Image.open(jpg_path)
        # 如果宽度小于高度 旋转270度
        if im.size[0] < im.size[1]:
            im = im.transpose(Image.Transpose.ROTATE_270)

        # 如果宽度不是高度的刚好两倍 则进行相应裁剪
        if im.size[0] / im.size[1] != 2:
            # 高度大于宽度的1/2 就裁剪高度
            if im.size[1] > im.size[0] / 2:
                im = im.crop((0, 0, im.size[0], im.size[0] // 2))
            else:
                # 高度小于宽度的1/2 且宽度高度都大于规格 就裁剪宽度到高度的两倍大小
                if im.size[0] >= size[0] and im.size[1] >= size[1]:
                    im = im.crop((0, 0, im.size[1] * 2, im.size[1]))

        # 其余情况就直接压缩直指定大小了
        im.resize((size[0], size[1]), Image.Resampling.BICUBIC).save(
            f'{save_path}/{uuid.uuid4()}.jpg', 'jpeg')

        os.remove(jpg_path)
