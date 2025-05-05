import pygame
import time
from settings import screen, BLACK, WHITE, font

def display_battle_info(text):
    """
    在屏幕底部显示战斗信息，如攻击的描述等。
    :param text: 需要显示的文本信息
    """
    battle_info = font.render(text, True, WHITE)
    screen.blit(battle_info, (200, 550))
    pygame.display.flip()  # 更新显示内容

def attack_animation(attacker, target, player_team, ai_team, background_img):
    """
    执行攻击动画，将攻击者移动到目标单位附近并返回原位。
    :param attacker: 发起攻击的单位
    :param target: 被攻击的目标单位
    :param player_team: 玩家单位队伍列表
    :param ai_team: AI单位队伍列表
    :param background_img: 背景图片
    """
    original_pos = attacker.position  # 保存攻击者的初始位置

    # 攻击动画，分10步进行
    for i in range(10):
        # 计算每一步攻击者的新位置
        attacker.position = (
            attacker.position[0] + (target.position[0] - original_pos[0]) // 10,
            attacker.position[1] + (target.position[1] - original_pos[1]) // 10
        )

        # 每一步重新绘制背景和所有单位
        screen.blit(background_img, (0, 0))  # 绘制背景图片

        # 绘制玩家和AI单位
        for unit in player_team + ai_team:
            unit.draw(screen)

        pygame.display.flip()  # 更新显示
        time.sleep(0.05)  # 控制攻击动画的速度，使动画更平滑

    attacker.position = original_pos  # 动画结束后恢复攻击者的初始位置