import pygame
import random
import os

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Screen
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Images
bgimg = pygame.image.load("bg.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
intro = pygame.image.load("intro.png")
intro = pygame.transform.scale(intro, (screen_width, screen_height)).convert_alpha()
outro = pygame.image.load("outro.png")
outro = pygame.transform.scale(outro, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)
big_font = pygame.font.SysFont(None, 72)

def text_screen(text, color, x, y, size=35):
    screen_text = pygame.font.SysFont(None, size).render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
        pygame.display.update()
        clock.tick(60)

def gameloop():
    exit_game = False
    game_over = False

    # Snake variables
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    snake_size = 30
    init_velocity = 5
    fps = 60

    # Food variables
    food_x = random.randint(20, screen_width - 50)
    food_y = random.randint(20, screen_height - 50)

    score = 0

    # Highscore file
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            
            gameWindow.blit(outro, (0, 0))
            
            # Display final score
            score_text = big_font.render(f"Score: {score}", True, white)
            score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
            gameWindow.blit(score_text, score_rect)
            
            # Display highscore in white
            highscore_text = big_font.render(f"Highscore: {highscore}", True, white)
            highscore_rect = highscore_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
            gameWindow.blit(highscore_text, highscore_rect)
            
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
                    # Prevent reversing direction
                    if event.key == pygame.K_RIGHT and velocity_x == 0:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT and velocity_x == 0:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP and velocity_y == 0:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN and velocity_y == 0:
                        velocity_y = init_velocity
                        velocity_x = 0

            # Move snake
            snake_x += velocity_x
            snake_y += velocity_y

            # Check food collision
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(20, screen_width - 50)
                food_y = random.randint(20, screen_height - 50)
                snk_length += 5
                if score > highscore:
                    highscore = score

            # Background and score
            gameWindow.blit(bgimg, (0, 0))
            text_screen(f"Score: {score}  Highscore: {highscore}", white, 5, 5)

            # Draw food
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            # Snake mechanics
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]

            # Check collision with self or walls
            if head in snk_list[:-1]:
                game_over = True
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
