import cv2
import numpy as np
import pyautogui
import os
from common.log import logger
def multi_scale_template_matching(screen, target_image, scales=None, threshold=0.8):
    if scales is None:
        scales = [0.7, 0.8,0.9, 1.0, 1.1, 1.2,1.3,1.4, 1.5]

    for scale in scales:
        # 调整图像大小
        resized_target = cv2.resize(target_image, (0, 0), fx=scale, fy=scale)
        target_height, target_width = resized_target.shape[:2]

        # 使用模板匹配
        result = cv2.matchTemplate(screen, resized_target, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            target_center = (max_loc[0] + target_width // 2, max_loc[1] + target_height // 2)
            return target_center, max_val
    return 0, max_val
    #     logger.info("result:{}".format(result))
    #     matches = []
    #     loc = np.where(result >= threshold)

    #     for pt in zip(*loc[::-1]):  # 匹配位置的坐标
    #         target_center = (pt[0] + target_width // 2, pt[1] + target_height // 2)
    #         matches.append(target_center)
    # return matches



def find_image_on_screen(target_image_path, threshold=0.8):
    # 读取目标图像并转换为灰度图像
    target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)

    # 截取屏幕图像并转换为灰度图像
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2GRAY)

    # 在多个尺度上进行模板匹配
    target_center, max_val = multi_scale_template_matching(screen, target_image, threshold=threshold)
    # 是否存在匹配值
    if target_center:
        print(f"Image found  at {target_center}")
        pyautogui.moveTo(target_center)
        return True,target_center
    else:
        print("Image not found on the screen.")
    return False,target_center

    # matches = multi_scale_template_matching(screen, target_image, threshold=threshold)
    # if len(matches)>0:
    #     print(f"Found {len(matches)} matches for {target_image_path}")
    #     return True, matches
    # else:
    #     print("Image not found on the screen.")
    #     return False, matches

def process_images(folder_path, key, config):
    """
    遍历文件夹，检查图片是否在屏幕上存在，并更新配置字典。
    
    :param folder_path: 图片所在文件夹的路径
    :param key: 配置字典中对应的键
    :param config: 配置字典
    """
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(folder_path, filename)
            iffind,_ = find_image_on_screen(image_path)
            if iffind:
                # 提取标号（假设标号是文件名的一部分，不含扩展名）
                logger.info("find {}".format(image_path))
                label = os.path.splitext(filename)[0]
                config[key].append(label)

def click(target_center):
    pyautogui.click(target_center)








if __name__ == "__main__":
    target_image_path = 'image/invite1.png'  # 替换为目标图像的路径
    # 点击开始
    
    # 初始化状态
        # 剩余玩家
        # 已经出牌
        # 玩家手牌情况

    # 局内游戏
    while True:
        print("a")
        # 识别手牌
        # 转换为文字信息
        # 将每一次的手牌
        # 对每一次别人出牌
        # # 判别自己是否可以杠牌或者胡牌
        # 对自己的出牌
        # 结合历史出牌信息和当前的出牌信息向大模型请求下一次出牌请求
        # 将出牌请求转换为鼠标动作
        # 验证最终出牌动作
    find_image_on_screen(target_image_path)