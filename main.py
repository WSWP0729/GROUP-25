import pygame  # 引入pygame库，用于游戏开发
import random  # 引入random库，用于生成随机数
import sys  # 引入sys库，用于退出程序
import logging  # 引入logging库，用于记录日志
import json  # 引入json库，用于保存和加载游戏数据
from settings import screen, BLACK, WHITE, font, background_img, attack_sound, SAVE_FILE  # 从settings文件中导入游戏设置
from screens import start_screen, setup_screen, game_over_screen  # 从screens文件中导入不同的游戏界面
from battle import attack_animation  # 从battle文件中导入攻击动画函数
from unit import Unit  # 从unit文件中导入Unit类

# 日志设置，配置日志记录的级别、格式和处理程序
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式，包括时间、日志级别和消息
    handlers=[
        logging.FileHandler("game_log.txt"),  # 将日志保存到文件game_log.txt中
        logging.StreamHandler()  # 在控制台输出日志
    ]
)

# 定义去重过滤器类，用于防止重复日志记录
class DeduplicationFilter(logging.Filter):
    last_log = ""  # 用于保存最后一条日志信息

    # 定义过滤器的filter方法
    def filter(self, record):
        current_log = record.getMessage()  # 获取当前日志消息
        if current_log == DeduplicationFilter.last_log:  # 如果当前日志与最后一条相同，返回False，表示不记录该日志
            return False
        DeduplicationFilter.last_log = current_log  # 更新最后一条日志消息
        return True  # 返回True，表示记录该日志

# 获取logger对象并添加去重过滤器
logger = logging.getLogger()
logger.addFilter(DeduplicationFilter())

# 定义游戏设置函数，用于初始化玩家和AI的队伍
def game_setup():
    player_team = setup_screen()  # 调用setup_screen函数获取玩家队伍
    ai_team = []  # 初始化AI队伍为空列表
    for i in range(3):  # 生成三个AI单位
        name = f"AI{random.randint(10, 99)}"  # 随机生成AI的名字
        unit_type = random.choice(['Warrior', 'Tank'])  # 随机选择单位类型
        position = (650, 100 + i * 200)  # 设置AI单位的位置
        ai_team.append(Unit(name, unit_type, position))  # 将生成的AI单位添加到AI队伍中
    return player_team, ai_team  # 返回玩家队伍和AI队伍

# 定义保存游戏函数，将当前游戏状态保存到文件中
def save_game(player_team, ai_team, player_gold):
    try:
        # 构建保存数据的字典
        save_data = {
            "player_team": [
                {"name": unit.name, "type": unit.unit_type, "position": list(unit.position), "hp": unit.hp}
                for unit in player_team
            ],
            "ai_team": [
                {"name": unit.name, "type": unit.unit_type, "position": list(unit.position), "hp": unit.hp}
                for unit in ai_team
            ],
            "player_gold": player_gold  # 保存玩家的金币数量
        }
        # 将数据写入保存文件中
        with open(SAVE_FILE, "w") as file:
            json.dump(save_data, file)
        logging.info("Game saved successfully to %s.", SAVE_FILE)  # 记录保存成功的日志
    except Exception as e:
        logging.error(f"Failed to save game: {e}")  # 如果保存失败，记录错误日志

# 定义加载游戏函数，从文件中加载保存的游戏状态
def load_game():
    try:
        # 从保存文件中读取数据
        with open(SAVE_FILE, "r") as file:
            save_data = json.load(file)
            # 重建玩家队伍和AI队伍
            player_team = [Unit(unit_data["name"], unit_data["type"], tuple(unit_data["position"])) for unit_data in save_data["player_team"]]
            for unit, unit_data in zip(player_team, save_data["player_team"]):
                unit.hp = unit_data["hp"]  # 恢复单位的生命值
            ai_team = [Unit(unit_data["name"], unit_data["type"], tuple(unit_data["position"])) for unit_data in save_data["ai_team"]]
            for unit, unit_data in zip(ai_team, save_data["ai_team"]):
                unit.hp = unit_data["hp"]  # 恢复AI单位的生命值
            player_gold = save_data.get("player_gold", 100)  # 获取玩家的金币数量，默认为100
            return player_team, ai_team, player_gold  # 返回加载的队伍和金币
    except FileNotFoundError:
        logging.error("No save file found.")  # 如果没有找到保存文件，记录错误日志
        return None, None, None  # 返回空值
    except Exception as e:
        logging.error(f"Failed to load game: {e}")  # 如果加载失败，记录错误日志
        return None, None, None  # 返回空值

# 定义游戏主循环函数，控制游戏的主要逻辑
def game_loop(player_team, ai_team, player_gold):
    current_turn = 'Player'  # 初始化当前回合为玩家
    selected_unit = None  # 初始化选中的单位为空
    running = True  # 控制游戏循环的标志位
    clock = pygame.time.Clock()  # 创建时钟对象，用于控制帧率
    recruit_button = pygame.Rect(screen.get_width() // 2 - 75, screen.get_height() // 2 - 25, 150, 50)  # 定义复活单位按钮的位置和大小
    save_button = pygame.Rect((screen.get_width() // 2) - 70, 20, 140, 50)  # 定义保存按钮的位置和大小

    while running:  # 游戏主循环
        screen.blit(background_img, (0, 0))  # 绘制背景图像
        gold_text = font.render(f"Gold: {player_gold}", True, (255, 215, 0))  # 绘制玩家金币文本
        gold_text_rect = gold_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))  # 设置金币文本的位置
        screen.blit(gold_text, gold_text_rect)  # 将金币文本绘制到屏幕上

        alive_player_team = [unit for unit in player_team if unit.hp > 0]  # 获取存活的玩家单位
        alive_ai_team = [unit for unit in ai_team if unit.hp > 0]  # 获取存活的AI单位
        dead_units = [unit for unit in player_team if unit.hp <= 0]  # 获取已死亡的玩家单位

        # 根据条件设置复活按钮的颜色（如果玩家金币足够且有死亡单位）
        button_color = (255, 0, 0) if player_gold >= 150 and dead_units else (128, 128, 128)
        pygame.draw.rect(screen, button_color, recruit_button)  #R绘制复活按钮
        recruit_text = font.render("Recruit (150g)", True, BLACK)  # 生成招募按钮的文本
        recruit_text_rect = recruit_text.get_rect(center=(recruit_button.centerx, recruit_button.centery))  # 设置复活按钮文本的位置
        screen.blit(recruit_text, recruit_text_rect)  # 将复活按钮文本绘制到屏幕上

        pygame.draw.rect(screen, (0, 128, 0), save_button)  # 绘制保存按钮
        save_text = font.render("Save", True, WHITE)  # 生成保存按钮的文本
        save_text_rect = save_text.get_rect(center=(save_button.centerx, save_button.centery))  # 设置保存按钮文本的位置
        screen.blit(save_text, save_text_rect)  # 将保存按钮文本绘制到屏幕上

        for event in pygame.event.get():  # 事件循环
            if event.type == pygame.QUIT:  # 如果接收到退出事件
                running = False  # 结束游戏循环
                pygame.quit()  # 关闭pygame
                sys.exit()  # 退出程序
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 如果检测到鼠标点击事件
                mouse_pos = event.pos  # 获取鼠标点击的位置
                if current_turn == 'Player':  # 如果当前是玩家的回合
                    if selected_unit is None:  # 如果没有选中单位
                        for unit in alive_player_team:  # 检查鼠标点击是否选中了玩家单位
                            if (mouse_pos[0] - unit.position[0]) ** 2 + (
                                    mouse_pos[1] - unit.position[1]) ** 2 <= 30 ** 2:
                                selected_unit = unit  # 将该单位设为选中
                                break
                    else:  # 如果已有选中的单位
                        for unit in alive_ai_team:  # 检查鼠标点击是否在AI单位范围内
                            if (mouse_pos[0] - unit.position[0]) ** 2 + (
                                    mouse_pos[1] - unit.position[1]) ** 2 <= 30 ** 2:
                                attack_sound.play()  # 播放攻击音效
                                attack_animation(selected_unit, unit, alive_player_team, alive_ai_team, background_img)  # 播放攻击动画
                                pygame.time.delay(1)  # 延迟1毫秒
                                selected_unit.attack(unit)  # 让选中的单位攻击目标单位
                                if unit.hp <= 0:  # 如果AI单位被击败
                                    player_gold += 50  # 玩家获得50金币奖励
                                    alive_ai_team.remove(unit)  # 从AI队伍中移除该单位
                                current_turn = 'AI'  # 切换回合至AI
                                selected_unit = None  # 重置选中的单位
                                break
                    if recruit_button.collidepoint(mouse_pos) and player_gold >= 150 and dead_units:  # 检查是否点击了复活按钮
                        player_gold -= 150  # 扣除150金币
                        revived_unit = dead_units.pop(0)  # 从死亡单位列表中取出一个单位
                        revived_unit.hp = revived_unit.max_hp  # 恢复该单位的生命值
                if save_button.collidepoint(mouse_pos):  # 检查是否点击了保存按钮
                    save_game(player_team, ai_team, player_gold)  # 调用保存游戏函数

        for unit in alive_player_team:  # 绘制存活的玩家单位
            unit.draw(screen)
        for unit in alive_ai_team:  # 绘制存活的AI单位
            unit.draw(screen)

        pygame.display.flip()  # 更新屏幕显示
        clock.tick(60)  # 控制帧率为60帧每秒

        if current_turn == 'AI' and alive_ai_team:  # 如果当前回合为AI且AI单位存活
            attacker = random.choice(alive_ai_team)  # 随机选择一个AI单位作为攻击者
            target = random.choice(alive_player_team)  # 随机选择一个玩家单位作为目标
            attack_sound.play()  # 播放攻击音效
            attack_animation(attacker, target, alive_player_team, alive_ai_team, background_img)  # 播放攻击动画
            pygame.time.delay(1)  # 延迟1毫秒
            attacker.attack(target)  # 攻击目标单位
            if target.hp <= 0:  # 如果目标单位被击败
                alive_player_team.remove(target)  # 从玩家队伍中移除该单位
            current_turn = 'Player'  # 切换回合至玩家

        if not alive_player_team or not alive_ai_team:  # 如果任意一方的队伍全灭
            running = False  # 结束游戏循环

    if alive_player_team:  # 如果玩家队伍仍有存活单位
        winner = "Player"  # 玩家获胜
    else:  # 否则
        winner = "AI"  # AI获胜

    result = game_over_screen(winner)  # 显示游戏结束界面并获取结果
    if result == "retry":  # 如果玩家选择重试
        player_team, ai_team = game_setup()  # 重新设置游戏
        game_loop(player_team, ai_team, player_gold)  # 重新进入游戏循环
def main():
    logging.info("Game started.")  # 记录游戏启动的信息日志
    choice = start_screen()  # 获取用户在开始界面上的选择（新游戏或加载游戏）

    if choice == "load_game":  # 如果用户选择加载游戏
        player_team, ai_team, player_gold = load_game()  # 尝试加载之前的游戏进度
        if player_team is None or ai_team is None:  # 如果没有找到保存的进度或加载失败
            player_team, ai_team = game_setup()  # 进入新的游戏设置
            player_gold = 100  # 初始化玩家金币为100
    else:  # 如果用户选择新游戏
        player_team, ai_team = game_setup()  # 设置新的游戏，创建玩家和AI的队伍
        player_gold = 100  # 初始化玩家金币为100

    game_loop(player_team, ai_team, player_gold)  # 开始游戏循环，传入玩家队伍、AI队伍和玩家金币
    pygame.quit()  # 退出pygame
    sys.exit()  # 退出程序

# 判断脚本是否直接运行，如果是，则调用main函数
if __name__ == "__main__":
    main()  # 运行游戏的主入口