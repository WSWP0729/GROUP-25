import pygame
import os
import logging

# 初始化Pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Turn-based Battle Game")

# 定义资源文件目录
BASE_DIR = os.path.dirname(__file__)  # 获取当前文件的目录
IMAGE_DIR = os.path.join(BASE_DIR, 'images')  # 图片文件夹路径
SOUND_DIR = os.path.join(BASE_DIR, 'sounds')  # 音效文件夹路径

# 加载图片资源
background_img = pygame.image.load(os.path.join(IMAGE_DIR, 'battle_background.png'))

# 加载音效资源
attack_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'attack_sound.wav'))

# 定义选择职业界面的背景图片路径
SETUP_SCREEN_BACKGROUND = os.path.join(IMAGE_DIR, 'setup_background.png')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# 字体设置
FONT_NAME = 'Arial'
FONT_SIZE = 25
font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

# 图片资源
START_SCREEN_IMG1 = os.path.join(IMAGE_DIR, 'image1.png')
START_SCREEN_IMG2 = os.path.join(IMAGE_DIR, 'image2.png')
LOAD_IMAGE = os.path.join(IMAGE_DIR, 'load_image.png')

# 音效资源
BACKGROUND_MUSIC = os.path.join(SOUND_DIR, 'background_music.mp3')
ATTACK_SOUND = os.path.join(SOUND_DIR, 'attack_sound.wav')

# 游戏设置
PLAYER_START_GOLD = 100

# 单位设置
UNIT_SIZE = (40, 40)
UNIT_HEALTH_WARRIOR = 100
UNIT_HEALTH_TANK = 150
UNIT_ATTACK_DAMAGE_WARRIOR = 20
UNIT_ATTACK_DAMAGE_TANK = 10

# 按钮设置
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_COLOR_ACTIVE = GREEN
BUTTON_COLOR_INACTIVE = RED

# 游戏状态
class GameState:
    START = 'start'
    SETUP = 'setup'
    BATTLE = 'battle'
    GAME_OVER = 'game_over'

# FPS设置
FPS = 60

# 日志设置
LOG_FILE = os.path.join(BASE_DIR, 'game_log.txt')
LOG_LEVEL = logging.INFO
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# 存档设置
SAVE_FILE = os.path.join(BASE_DIR, 'save_file.json')

# 初始化混音器
pygame.mixer.init()

# 设置音量
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.7
pygame.mixer.music.set_volume(MUSIC_VOLUME)
attack_sound.set_volume(SFX_VOLUME)

# 播放背景音乐
def play_background_music():
    try:
        pygame.mixer.music.load(BACKGROUND_MUSIC)
        pygame.mixer.music.play(-1)  # -1 表示循环播放
        logging.info("Background music started playing.")
    except pygame.error as e:
        logging.error(f"Failed to play background music: {e}")

play_background_music()