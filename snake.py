import pygame
from pygame.locals import *
import random
import time

# Initialize Pygame
pygame.init()

# Define constants
COLUMNS = 40
ROWS = 40
CELL_SIZE = 20
WINDOW_WIDTH = COLUMNS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define font
font = pygame.font.Font(None, 36)


def reset_game():
    global snake_pos, food_pos, direction, game_over, score, fps
    snake_pos = [(COLUMNS // 2, ROWS // 2 + i) for i in range(5)]
    food_pos = (random.randint(1, COLUMNS - 2), random.randint(1, ROWS - 2))
    direction = (0, -1)
    game_over = False
    score = 0
    fps = 10


def draw_menu():
    screen.fill(BLACK)
    title = font.render("Snake Game", True, WHITE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
    screen.blit(title, title_rect)

    instructions = font.render("Press Enter to start or replay", True, WHITE)
    instructions_rect = instructions.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(instructions, instructions_rect)

    pygame.display.update()


def game_loop():
    # Added food_pos to the global variables
    global direction, game_over, score, fps, food_pos

    # Game loop
    clock = pygame.time.Clock()
    while not game_over:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                game_over = True
            elif event.type == KEYDOWN:
                if event.key == K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Move the snake
        new_head = (
            (snake_pos[0][0] + direction[0]) % COLUMNS,
            (snake_pos[0][1] + direction[1]) % ROWS,
        )
        snake_pos.insert(0, new_head)

        # Check for collisions
        if (
            new_head in snake_pos[1:]
            or new_head[0] < 1
            or new_head[0] >= COLUMNS - 1
            or new_head[1] < 1
            or new_head[1] >= ROWS - 1
        ):
            game_over = True

        # Check for food
        if new_head == food_pos:
            score += 1
            if score % 9 == 0:
                fps += 5
            food_pos = (random.randint(1, COLUMNS - 2),
                        random.randint(1, ROWS - 2))
        else:
            snake_pos.pop()

        # Draw the game
        screen.fill(BLACK)
        for x in range(COLUMNS):
            for y in range(ROWS):
                rect = pygame.Rect(x * CELL_SIZE, y *
                                   CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if (x, y) in snake_pos:
                    color = GREEN if (x, y) == snake_pos[0] else BLUE
                    pygame.draw.rect(screen, color, rect)
                elif (x, y) == food_pos:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, BLACK, rect, 1)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(topleft=(10, 10))
        screen.blit(score_text, score_rect)

        pygame.display.update()
        clock.tick(fps)

    # Game over message
    game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
    game_over_rect = game_over_text.get_rect(
        center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.update()

    # Wait for user input to replay or quit
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    reset_game()
                    draw_menu()
                    game_loop()
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    return


# Start the game
reset_game()
draw_menu()
game_loop()
