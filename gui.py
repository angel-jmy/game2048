import pygame
from functions import (
    new_board, move_left, move_right, move_up, move_down,
    spawn_tile, has_move, won
)

# --- CONFIG ---
CELL_SIZE = 100
CELL_MARGIN = 10
FONT_NAME = "arial"
BG_COLOR = (187, 173, 160)
EMPTY_COLOR = (205, 193, 180)
TEXT_COLOR = (119, 110, 101)
TOP_OFFSET = 50 # For displaying scores

# tile colors (add more as you like)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

def draw_board(screen, board, font, score):
    size = len(board)
    screen.fill(BG_COLOR)
    font_score = pygame.font.SysFont(FONT_NAME, 26)

    # Draw scores
    score_text = font_score.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 10))  # small offset from top-left

    # Draw grid below score
    # top_offset = 60  # space for score text
    for r in range(size):
        for c in range(size):
            val = board[r][c]
            color = TILE_COLORS.get(val, EMPTY_COLOR)
            x = c * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
            y = r * (CELL_SIZE + CELL_MARGIN) + TOP_OFFSET
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            if val != 0:
                text = font.render(str(val), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption("2048")

    board = new_board()
    size = len(board)
    width = size * (CELL_SIZE + CELL_MARGIN) + CELL_MARGIN
    height = width + TOP_OFFSET
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont(FONT_NAME, 40)

    running = True
    clock = pygame.time.Clock()

    # Initialize the score
    scores = 0

    while running:
        draw_board(screen, board, font, scores)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new, score, moved = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    new, score, moved = move_right(board)
                elif event.key == pygame.K_UP:
                    new, score, moved = move_up(board)
                elif event.key == pygame.K_DOWN:
                    new, score, moved = move_down(board)
                else:
                    continue

                if moved:
                    board = new
                    scores += score
                    spawn_tile(board)
                    if won(board):
                        print("🎉 You won!")
                        running = False
                    elif not has_move(board):
                        print("💀 Game over!")
                        running = False

        clock.tick(30)  # limit FPS

    pygame.quit()


if __name__ == "__main__":
    main()
