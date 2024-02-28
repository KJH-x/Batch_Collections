from PIL import Image

def merge_images(color_image_path, alpha_image_path, output_image_path):
    # 打开两个图像
    color_img = Image.open(color_image_path)
    alpha_img = Image.open(alpha_image_path)

    # 将alpha图像转换为带有Alpha通道的图像
    alpha_img = alpha_img.convert('L')

    # 确保两个图像的大小相同
    if color_img.size != alpha_img.size:
        raise ValueError("Color image and alpha image must have the same size")

    # 将alpha图像作为alpha通道添加到color图像上
    color_img.putalpha(alpha_img)

    # 保存结果
    color_img.save(output_image_path)

# 示例用法
# for text in ["battle_finish_hub#0","bossrush_relic#0","bossrush_stage#0"]:
#     color_image_path = rf'P:\BossRush_uiPack_common\[uc]bossrush\{text}s.png'
#     alpha_image_path = rf'P:\BossRush_uiPack_common\[uc]bossrush\{text}a.png'
#     output_image_path = rf'P:\BossRush_uiPack_common\[uc]bossrush\{text}.png'
#     # bossrush_milestone#0.png bossrush_milestone#1
#     merge_images(color_image_path, alpha_image_path, output_image_path)
# p:\BossRush_uiPack_common\bossrush\battle\act1bossrush_battle_ui_plugin\bossrush_atlas#0a.png
    
color_image_path = rf'p:\new_attach\Unpacked_1708870773\Android\activity\[uc]act4bossrush\squad_plugin_atlas#0s.png'
alpha_image_path = rf'p:\new_attach\Unpacked_1708870773\Android\activity\[uc]act4bossrush\squad_plugin_atlas#0a.png'
output_image_path = rf'p:\new_attach\Unpacked_1708870773\Android\activity\[uc]act4bossrush\squad_plugin_atlas#0.png'
# bossrush_milestone#0.png bossrush_milestone#1
merge_images(color_image_path, alpha_image_path, output_image_path)