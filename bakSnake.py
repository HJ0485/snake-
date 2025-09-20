import pygame
import random
import os

pygame.mixer.init()
pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
snakegreen = (35, 45, 40)

bg1 = pygame.image.load("Screen/bg.jpg")
bg2 = pygame.image.load("Screen/bg2.jpg")
intro = pygame.image.load("Screen/intro1.png")
outro = pygame.image.load("Screen/outro.png")

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Snake Game")
pygame.display.update()

pygame.mixer.music.load('music/wc.mp3')
pygame.mixer.music.play(100)
pygame.mixer.music.set_volume(.6)

clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 35)
big_font = pygame.font.SysFont('Harrington', 70)

def text_screen(text, color, x, y, use_big=False):
    if use_big:
        screen_text = big_font.render(text, True, color)
    else:
        screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load('music/bgm.mp3')
                    pygame.mixer.music.play(100)
                    pygame.mixer.music.set_volume(.6)
                    gameloop()
        pygame.display.update()
        clock.tick(60)

def gameloop():
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width // 2)
    food_y = random.randint(20, screen_height // 2)

    score = 0
    init_velocity = 5
    snake_size = 30
    fps = 60

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.blit(outro, (0, 0))

            # Show Score on the right side (empty box area)
            score_text = big_font.render(f"Score: {score}", True, white)
            score_rect = score_text.get_rect(center=(700, 300))  # X=700, Y=300 approx inside the box
            gameWindow.blit(score_text, score_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_q:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 10
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 5
                if score > int(highscore):
                    highscore = score

            gameWindow.blit(bg2, (0, 0))
            text_screen("Score: " + str(score) + "  Highscore: " + str(highscore), snakegreen, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('music/bgm1.mp3')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.6)

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('music/bgm2.mp3')
                pygame.mixer.music.play(100)
                pygame.mixer.music.set_volume(.6)

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
