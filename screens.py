import pygame
import logging
import sys
from settings import screen, BLACK, WHITE, font, START_SCREEN_IMG1, START_SCREEN_IMG2, LOAD_IMAGE, SETUP_SCREEN_BACKGROUND
from unit import Unit

def start_screen():
    logging.info("Entered start screen.")
    # 加载开始界面所需的图像
    image1 = pygame.image.load(START_SCREEN_IMG1)
    image2 = pygame.image.load(START_SCREEN_IMG2)
    load_image = pygame.image.load(LOAD_IMAGE)

    # 定义图像位置
    image1_rect = image1.get_rect(topleft=(0, 0))
    image2_rect = image2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    load_image_rect = load_image.get_rect(center=(screen.get_width() - 100, screen.get_height() - 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game quit from start screen.")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if load_image_rect.collidepoint(event.pos):
                    logging.info("Load game button clicked.")
                    return "load_game"
                elif image2_rect.collidepoint(event.pos):
                    logging.info("New game started.")
                    return "new_game"

        # 绘制图像
        screen.fill(BLACK)
        screen.blit(image1, image1_rect)
        screen.blit(image2, image2_rect)
        screen.blit(load_image, load_image_rect)
        pygame.display.flip()


def setup_screen():
    logging.info("Entered setup screen.")
    # 加载并绘制背景图片
    background_img = pygame.image.load(SETUP_SCREEN_BACKGROUND)

    input_boxes = [pygame.Rect(350, 50 + i * 200, 140, 40) for i in range(3)]
    input_texts = [""] * 3
    selected_types = [""] * 3
    running = True

    def draw_setup_screen():
        # 绘制背景图片
        screen.blit(background_img, (0, 0))

        for i in range(3):
            pygame.draw.rect(screen, WHITE, (50, 50 + i * 200, 100, 50))
            pygame.draw.rect(screen, WHITE, (200, 50 + i * 200, 100, 50))
            pygame.draw.rect(screen, WHITE, input_boxes[i], 2)
            name_text = font.render(f"Name {i + 1}", True, WHITE)
            warrior_text = font.render("Warrior", True, BLACK)
            tank_text = font.render("Tank", True, BLACK)
            screen.blit(name_text, (50, 20 + i * 200))
            screen.blit(warrior_text, (50, 50 + i * 200))
            screen.blit(tank_text, (200, 50 + i * 200))
            if input_texts[i]:
                name_input = font.render(input_texts[i], True, WHITE)
                screen.blit(name_input, (input_boxes[i].x + 5, input_boxes[i].y + 5))
            if selected_types[i]:
                type_text = font.render(selected_types[i], True, WHITE)
                screen.blit(type_text, (500, 50 + i * 200))
        pygame.display.flip()

    current_input = 0
    input_active = [False] * 3

    while running and ("" in input_texts or "" in selected_types):
        draw_setup_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game quit during setup screen.")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i in range(3):
                    if input_boxes[i].collidepoint(mouse_pos):
                        input_active[i] = True
                        current_input = i
                    else:
                        input_active[i] = False
                    if 50 <= mouse_pos[0] <= 150 and 50 + i * 200 <= mouse_pos[1] <= 100 + i * 200:
                        selected_types[i] = 'Warrior'
                        logging.info(f"Player selected Warrior for character {i + 1}.")
                    elif 200 <= mouse_pos[0] <= 300 and 50 + i * 200 <= mouse_pos[1] <= 100 + i * 200:
                        selected_types[i] = 'Tank'
                        logging.info(f"Player selected Tank for character {i + 1}.")
            elif event.type == pygame.KEYDOWN and input_active[current_input]:
                if event.key == pygame.K_RETURN:
                    input_active[current_input] = False
                    logging.info(
                        f"Player confirmed name for character {current_input + 1}: {input_texts[current_input]}.")
                elif event.key == pygame.K_BACKSPACE:
                    input_texts[current_input] = input_texts[current_input][:-1]
                else:
                    input_texts[current_input] += event.unicode
                draw_setup_screen()

    player_team = []
    for i in range(3):
        position = (150, 100 + i * 200)
        player_team.append(Unit(input_texts[i], selected_types[i], position))
        logging.info(f"Created character {i + 1}: Name={input_texts[i]}, Type={selected_types[i]}.")

    return player_team

# 下面这一部分是cyx的内容1
def game_over_screen(winner):
    logging.info(f"Displaying game over screen. Winner: {winner}.")
    running = True
    retry_button = pygame.Rect(250, 400, 150, 50)
    quit_button = pygame.Rect(450, 400, 150, 50)

    while running:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        winner_text = font.render(f"{winner} Wins!", True, WHITE)
        screen.blit(game_over_text, (320, 200))
        screen.blit(winner_text, (320, 250))
        pygame.draw.rect(screen, (0, 255, 0), retry_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)
        retry_text = font.render("Retry", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)
        screen.blit(retry_text, (retry_button.x + 40, retry_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Game quit from game over screen.")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    logging.info("Retry selected from game over screen.")
                    return "retry"
                elif quit_button.collidepoint(event.pos):
                    logging.info("Quit selected from game over screen.")
                    pygame.quit()
                    sys.exit()