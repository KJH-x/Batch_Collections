import shutil
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import concurrent.futures


def create_thumbnail_with_name_overlay(image_path, output_folder):
    """
    创建规范化的缩略图并在底部填充黑色色块，叠画文件名

    :param image_path: 图片文件的完整路径
    :param output_folder: 处理后图片保存的文件夹
    """
    os.makedirs(output_folder, exist_ok=True)

    with Image.open(image_path) as img:
        # 获取原始图片的尺寸
        width, height = img.size

        # 计算缩略图的宽度，使得高度等比缩放为150
        unnamed_thumbnail_height = 150
        unnamed_thumbnail_width = int(
            width * unnamed_thumbnail_height / height)

        unnamed_thumbnail = img.resize(
            (unnamed_thumbnail_width, unnamed_thumbnail_height), Image.LANCZOS)

        # 对于宽度小于200的图片，在两侧填充黑色使其宽度变为200
        if unnamed_thumbnail_width < 200:
            left_padding = (200 - unnamed_thumbnail_width) // 2
            right_padding = 200 - unnamed_thumbnail_width - left_padding
            unnamed_thumbnail = ImageOps.expand(unnamed_thumbnail, border=(
                left_padding, 0, right_padding, 0), fill="black")

        # 对于缩放至高度150时宽度大于200的图片，居中裁切至宽度200
        elif unnamed_thumbnail_width > 200:
            left_crop = (unnamed_thumbnail_width - 200) // 2
            right_crop = unnamed_thumbnail_width - left_crop - 200
            unnamed_thumbnail = unnamed_thumbnail.crop(
                (left_crop, 0, unnamed_thumbnail_width - right_crop, unnamed_thumbnail_height))

        # 在底部添加黑色色块
        unnamed_thumbnail_width = 200
        new_height = unnamed_thumbnail_height + 50
        named_thumbnail = Image.new(
            "RGB", (unnamed_thumbnail_width, new_height), color="black")

        named_thumbnail.paste(unnamed_thumbnail, (0, 0))

        # 在底部色块中居中添加文件名
        draw = ImageDraw.Draw(named_thumbnail)
        font = ImageFont.truetype("arial.ttf", 40)
        file_name = os.path.splitext(os.path.basename(image_path))[0]

        text_left, text_top, text_right, text_bottom = draw.textbbox(
            (0, 0), text=file_name, font=font)
        text_width = abs(text_right - text_left)
        text_height = abs(text_top - text_bottom)
        text_position = ((unnamed_thumbnail_width - text_width) //
                         2, unnamed_thumbnail_height)

        draw.text(text_position, file_name, fill="white", font=font)

        # 构建保存路径
        image_filename = os.path.basename(image_path)
        output_path = os.path.join(output_folder, image_filename)

        # 保存处理后的图片
        named_thumbnail.save(output_path)


def combine_thumbnails(thumbnails_folder: str, output_folder: str) -> None:
    # 获取所有缩略图的路径
    thumbnail_paths = [os.path.join(thumbnails_folder, filename) for filename in os.listdir(
        thumbnails_folder) if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    if not thumbnail_paths:
        return

    # 计算大缩略图的行数和列数，使得尺寸接近方形
    num_images = len(thumbnail_paths)
    num_rows = int(num_images ** 0.5) + 1
    num_columns = (num_images + num_rows - 1) // num_rows

    # 计算大缩略图的尺寸
    with Image.open(thumbnail_paths[0]) as sample_thumbnail:
        thumbnail_width, thumbnail_height = sample_thumbnail.size

    big_thumbnail_width = num_columns * thumbnail_width
    big_thumbnail_height = num_rows * thumbnail_height

    big_thumbnail = Image.new(
        "RGB", (big_thumbnail_width, big_thumbnail_height), color="black")

    for i, thumbnail_path in enumerate(thumbnail_paths):
        row = i // num_columns
        col = i % num_columns
        with Image.open(thumbnail_path) as thumbnail:
            big_thumbnail.paste(
                thumbnail, (col * thumbnail_width, row * thumbnail_height))

    output_filename = "全图片缩略图.png"
    output_path = os.path.join(output_folder, output_filename)
    big_thumbnail.save(output_path)

    return


if __name__ == "__main__":
    image_folder = input("请指定工作目录：")
    output_folder = os.path.join(image_folder, ".thumbnails")

    # 删除之前存在的.name以及合并缩略图
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    combined_thumbnail_path = os.path.join(
        image_folder, "全图片缩略图.png")
    if os.path.exists(combined_thumbnail_path):
        os.remove(combined_thumbnail_path)

    # 枚举文件夹内的图片，并行处理
    image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(
        image_folder) if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        for image_path in image_paths:
            executor.submit(create_thumbnail_with_name_overlay,
                            image_path, output_folder)

    combine_thumbnails(output_folder, image_folder)
