import hashlib
import os
import re
import time


def get_md5(image_path):
    # 计算处理后的图片的MD5哈希值
    with open(image_path, 'rb') as file:
        md5 = hashlib.md5(file.read()).hexdigest()
        print(f"MD5哈希值: {md5}")


def change_md5_folder(root_folder):
    """
    修改文件中所有文件MD5
    """
    # 递归遍历文件夹及其子文件夹中的所有文件
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            # 获取图片文件的完整路径
            image_path = os.path.join(foldername, filename)
            # 调用处理图片的函数
            change_md5_file(image_path)


def change_md5_file(file_path):
    """
    修改文件MD5，在末尾添加时间戳来改变MD5
    """
    # 读取图片二进制数据
    with open(file_path, "rb") as file:
        file_data = file.read()

    # 使用正则表达式匹配以 "KK" 开头和以数字结尾的模式
    match = re.search(b"KK\\d+$", file_data)
    timestamp = str(int(time.time())).encode()  # 获取当前时间戳并转换为字节
    if match:
        # 如果匹配到 "KK" 开头和数字结尾的模式，将数字替换为时间戳
        new_image_data = re.sub(b"KK\\d+$", b"KK" + timestamp, file_data)
    else:
        # 如果没有匹配到模式，添加 "KK" 时间戳
        new_image_data = file_data + b"KK" + timestamp

    # 保存新的文件
    output_path = file_path
    with open(output_path, "wb") as output_image_file:
        output_image_file.write(new_image_data)
    print(f"已处理并保存为 {output_path}")


if __name__ == '__main__':
    change_md5_folder('/Users/alen/Aproject/flutter_project/assets')
