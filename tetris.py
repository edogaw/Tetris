import pygame
import random

# Initialize Pygame
pygame.init()

# Screen and Grid Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 750
PLAY_WIDTH, PLAY_HEIGHT = 300, 600  # 10 columns, 20 rows
BLOCK_SIZE = 30
TOP_LEFT_X = (SCREEN_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = SCREEN_HEIGHT - PLAY_HEIGHT - 50

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)

# Shapes and Colors
SHAPES = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],
    
    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],
    
    [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],
    
    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],
    
    [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....']],
    
    [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....']],
    
    [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....']]
]

SHAPE_COLORS = [
    (0, 255, 0), (255, 0, 0), (0, 255, 255),
    (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)
]

# Piece Class
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = SHAPE_COLORS[SHAPES.index(shape)]
        self.rotation = 0

# Grid and Piece Handling
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid

def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape_format):
        for j, column in enumerate(line):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    return [(x - 2, y - 4) for x, y in positions]

def valid_space(piece, grid):
    accepted_positions = [
        (x, y) for y in range(20) for x in range(10) if grid[y][x] == BLACK
    ]
    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    return any(y < 1 for x, y in positions)

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

# Drawing Functions
def draw_grid(surface):
    for i in range(20):
        pygame.draw.line(surface, GREY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(10):
        pygame.draw.line(surface, GREY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))

def draw_window(surface, grid):
    surface.fill(BLACK)
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', True, WHITE)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH // 2 - label.get_width() // 2, 30))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (TOP_LEFT_X + x * BLOCK_SIZE, TOP_LEFT_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    draw_grid(surface)
    pygame.draw.rect(surface, RED, (TOP_LEFT_X, TOP_LEFT_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)
    pygame.display.update()

# Main Game Loop
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    run = True

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # Piece Falling
        if fall_time / 1000 >= 0.3:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()

                if check_lost(locked_positions):
                    run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        draw_window(screen, grid)

main()
