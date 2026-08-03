import pygame
import random
import sys

# ============================================
# CONSTANTS
# ============================================
WIDTH = 600
HEIGHT = 600
BLOCK_SIZE = 20
FPS = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
GRAY = (50, 50, 50)

# ============================================
# INITIALIZATION
# ============================================
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")
clock = pygame.time.Clock()

font_small = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 72)


def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)


def show_score(score):
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def show_game_over(score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    go_text = font_large.render("GAME OVER", True, RED)
    go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
    screen.blit(go_text, go_rect)

    score_text = font_small.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
    screen.blit(score_text, score_rect)

    restart_text = font_small.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 90))
    screen.blit(restart_text, restart_rect)


def get_random_food_position(snake):
    while True:
        x = random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE
        if [x, y] not in snake:
            return [x, y]


def reset_game():
    global snake, direction, next_direction, food, score
    start_x = (WIDTH // 2 // BLOCK_SIZE) * BLOCK_SIZE
    start_y = (HEIGHT // 2 // BLOCK_SIZE) * BLOCK_SIZE
    snake = [
        [start_x, start_y],
        [start_x - BLOCK_SIZE, start_y],
        [start_x - (BLOCK_SIZE * 2), start_y]
    ]
    direction = 'RIGHT'
    next_direction = 'RIGHT'
    food = get_random_food_position(snake)
    score = 0


reset_game()


def main():
    global direction, next_direction, snake, food, score

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        reset_game()
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        next_direction = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        next_direction = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        next_direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        next_direction = 'RIGHT'

        if game_over:
            screen.fill(BLACK)
            draw_grid()
            for i, segment in enumerate(snake):
                color = DARK_GREEN if i == 0 else GREEN
                pygame.draw.rect(screen, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            show_score(score)
            show_game_over(score)
            pygame.display.update()
            clock.tick(FPS)
            continue

        direction = next_direction
        head = snake[0].copy()

        if direction == 'UP':
            head[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            head[1] += BLOCK_SIZE
        elif direction == 'LEFT':
            head[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head[0] += BLOCK_SIZE

        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT):
            game_over = True
            continue

        if head in snake[1:]:
            game_over = True
            continue

        ate_food = False
        if head == food:
            ate_food = True
            score += 1
            food = get_random_food_position(snake)

        if ate_food:
            snake.insert(0, head)
        else:
            snake.insert(0, head)
            snake.pop()

        screen.fill(BLACK)
        draw_grid()

        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        for i, segment in enumerate(snake):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(screen, color, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            
            if i == 0:
                eye_size = 4
                if direction == 'RIGHT':
                    pygame.draw.circle(screen, WHITE, (segment[0] + 14, segment[1] + 4), eye_size)
                    pygame.draw.circle(screen, WHITE, (segment[0] + 14, segment[1] + 14), eye_size)
                elif direction == 'LEFT':
                    pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + 4), eye_size)
                    pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + 14), eye_size)
                elif direction == 'UP':
                    pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + 4), eye_size)
                    pygame.draw.circle(screen, WHITE, (segment[0] + 14, segment[1] + 4), eye_size)
                elif direction == 'DOWN':
                    pygame.draw.circle(screen, WHITE, (segment[0] + 4, segment[1] + 14), eye_size)
                    pygame.draw.circle(screen, WHITE, (segment[0] + 14, segment[1] + 14), eye_size)

        show_score(score)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()