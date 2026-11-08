import pygame

TILE = 40
COLS, ROWS = 12, 8
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

GRID = [[pygame.Color(40, 44, 52) for _ in range(COLS)] for _ in range(ROWS)]
HIGHLIGHT = pygame.Color(255, 200, 80)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()          # NOT clamped to the window
    col = mx // TILE
    row = my // TILE
    hovered_color = GRID[row][col].lerp(pygame.Color("white"), 0.4)   # the innocent line

    screen.fill((18, 18, 20))
    for r in range(ROWS):
        for c in range(COLS):
            color = hovered_color if (r, c) == (row, col) else GRID[r][c]
            pygame.draw.rect(screen, color, (c * TILE, r * TILE, TILE - 2, TILE - 2))

    pygame.display.flip()
    clock.tick(60)
