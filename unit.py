import pygame
import random
import logging
from settings import WHITE, font, IMAGE_DIR

class Unit:
    def __init__(self, name, unit_type, position):
        """
        初始化单位（角色）的属性。
        :param name: 角色名称
        :param unit_type: 角色类型（如Warrior或Tank）
        :param position: 角色在屏幕上的位置
        """
        self.name = name
        self.unit_type = unit_type
        self.hp = 100  # 初始生命值
        self.exp = 0  # 初始经验值
        self.level = 1  # 初始等级
        self.position = (position[0], position[1] + 30)  # 初始位置的调整
        self.max_hp = 100  # 最大生命值

        # 根据角色类型设置不同的攻击力、防御力和图像
        if unit_type == 'Warrior':
            self.defense = random.randint(1, 10)
            self.image = pygame.image.load(f"{IMAGE_DIR}/warrior.png")
        elif unit_type == 'Tank':
            self.atk = random.randint(20, 30)
            self.defense = random.randint(5, 15)
            self.image = pygame.image.load(f"{IMAGE_DIR}/tank.png")

    def attack(self, target):
        """
        执行攻击操作，对目标单位造成伤害，并增加攻击者的经验值。
        :param target: 被攻击的目标单位
        """
        damage = self.atk - target.defense + random.randint(-5, 10)
        damage = max(0, damage)  # 确保伤害值不为负
        target.hp -= damage  # 减少目标的生命值
        self.exp += damage  # 增加攻击者的经验值

        # 检查攻击者是否升级
        if self.exp >= 100:
            self.level_up()

        logging.info(f"{self.name} attacked {target.name} for {damage} damage.")

    def level_up(self):
        """
        当经验值达到100时，角色升级，等级提升，经验值清零。
        """
        self.level += 1
        self.exp -= 100  # 升级后经验值减去100
        logging.info(f"{self.name} leveled up to {self.level}!")

    def draw(self, screen):
        """
        在屏幕上绘制单位的图像、生命值、等级和经验值。
        :param screen: Pygame屏幕对象
        """
        self.draw_health_bar(screen)  # 绘制生命条

        # 绘制单位的图像
        screen.blit(self.image,
                    (self.position[0] - self.image.get_width() // 2, self.position[1] - self.image.get_height() // 2))

        # 绘制单位的生命值
        hp_text = font.render(f"{self.name} HP: {self.hp}", True, WHITE)
        screen.blit(hp_text, (self.position[0] - 40, self.position[1] - 50))

        # 绘制单位的等级
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(level_text, (self.position[0] - 40, self.position[1] - 70))

        # 绘制单位的经验值
        exp_text = font.render(f"EXP: {self.exp}", True, WHITE)
        screen.blit(exp_text, (self.position[0] - 40, self.position[1] - 90))

    def draw_health_bar(self, screen):
        """
        在单位图像的上方绘制生命条，显示当前的生命值。
        :param screen: Pygame屏幕对象
        """
        # 计算血条的宽度和高度
        bar_width = self.image.get_width()
        bar_height = 5

        # 计算血条的位置
        bar_x = self.position[0] - bar_width // 2
        bar_y = self.position[1] - self.image.get_height() // 2 - 10  # 血条在单位头上10像素处

        # 计算血条的填充比例
        hp_ratio = self.hp / self.max_hp

        # 绘制血条背景（红色，表示失去的生命值）
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # 绘制当前血量的部分（绿色）
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))