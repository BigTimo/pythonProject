import shutil

from PIL import Image, ImageDraw, ImageOps
import os

# 设计图路径
icon_path = "icon.png"

# Flutter项目路径
project_path = "/Users/alen/Aproject/flutter_project"
ios_icon_path = f"{project_path}/ios/Runner/Assets.xcassets/AppIcon.appiconset"
android_icon_path = f"{project_path}/android/app/src/main/res"
android_icon_name = "ic_launcher.png"
android_icon_round_name = "ic_launcher_round.png"

# android 尺寸
icon_size_android = {
    "mipmap-xxxhdpi": 192,
    "mipmap-xxhdpi": 144,
    "mipmap-xhdpi": 96,
    "mipmap-hdpi": 72,
    "mipmap-mdpi": 48,
    "mipmap-ldpi": 36,
}
# ios尺寸
icon_size_ios = [29, 40, 57, 58, 60, 80, 87, 114, 120, 180, 1024]


def gen_icon_android(input_image_path):
    """
    生成android方形和圆形图标
    """

    # 打开原始图片
    input_image = Image.open(input_image_path)

    # 创建图标文件夹并生成图标
    for folder_name, size in icon_size_android.items():
        # 生成对应文件夹
        output_folder = os.path.join(android_icon_path, folder_name)
        os.makedirs(output_folder, exist_ok=True)

        # 方形图标处理：直接保存为对应尺寸
        square_icon = input_image.resize((size, size))
        square_icon_path = os.path.join(output_folder, android_icon_name)
        square_icon.save(square_icon_path, 'PNG')

        # 圆形图标处理：裁剪成圆形，再保存为对应尺寸
        circular_icon = input_image.copy()
        min_side = min(circular_icon.width, circular_icon.height)
        circular_icon = circular_icon.crop((0, 0, min_side, min_side))
        mask = Image.new("L", circular_icon.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, circular_icon.width, circular_icon.height), fill=255)
        circular_icon = ImageOps.fit(circular_icon, mask.size, centering=(0.5, 0.5))
        circular_icon.putalpha(mask)
        circular_icon = circular_icon.resize((size, size))
        circular_icon_path = os.path.join(output_folder, android_icon_round_name)
        circular_icon.save(circular_icon_path, 'PNG')

    input_image.close()


def gen_icon_ios(input_image_path):
    """
    生成ios图标和各尺寸配置文件
    """

    folder = ios_icon_path
    clear_folder(folder)
    copy_file("Contents.json", folder)

    # 打开输入图片
    img = Image.open(input_image_path)

    # 生成不同尺寸的图片
    for size in icon_size_ios:
        output_image_path = os.path.join(folder, f"{size}.png")
        resized_img = img.resize((size, size))
        resized_img.save(output_image_path)
        resized_img.close()
    img.close()


def clear_folder(folder_path):
    # 检查文件夹是否存在，如果存在则删除
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    # 创建新的文件夹
    os.makedirs(folder_path, exist_ok=True)


def copy_file(source_file, destination_folder):
    # 确保目标文件夹存在
    os.makedirs(destination_folder, exist_ok=True)
    # 使用shutil复制文件到目标文件夹
    shutil.copy(source_file, destination_folder)


if __name__ == '__main__':
    gen_icon_android(icon_path)
    gen_icon_ios(icon_path)
