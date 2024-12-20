import pygame
import random

# initialize Pygame
pygame.init()

# window size
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = SCREEN_WIDTH // BLOCK_SIZE, SCREEN_HEIGHT // BLOCK_SIZE

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

COLORS = [CYAN, BLUE, ORANGE, YELLOW, GREEN, MAGENTA, RED]

# define shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
]

class Tetris:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0  # initialize score
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color, "x": COLS // 2 - len(shape[0]) // 2, "y": 0}

    def rotate_piece(self):
        shape = self.current_piece["shape"]
        self.current_piece["shape"] = [list(row) for row in zip(*shape[::-1])]

    def move_piece(self, dx, dy):
        self.current_piece["x"] += dx
        self.current_piece["y"] += dy
        if self.check_collision():
            self.current_piece["x"] -= dx
            self.current_piece["y"] -= dy

    def check_collision(self):
        shape = self.current_piece["shape"]
        x, y = self.current_piece["x"], self.current_piece["y"]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    if x + j < 0 or x + j >= COLS or y + i >= ROWS or self.board[y + i][x + j]:
                        return True
        return False

    def lock_piece(self):
        shape = self.current_piece["shape"]
        x, y = self.current_piece["x"], self.current_piece["y"]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[y + i][x + j] = self.current_piece["color"]
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        if self.check_collision():
            self.game_over = True

    def clear_lines(self):
        cleared_lines = 0
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared_lines = ROWS - len(new_board)  # calculate cleared rows
        while len(new_board) < ROWS:
            new_board.insert(0, [0] * COLS)
        self.board = new_board

        # update score
        if cleared_lines == 1:
            self.score += 100
        elif cleared_lines == 2:
            self.score += 300
        elif cleared_lines == 3:
            self.score += 500
        elif cleared_lines == 4:
            self.score += 800

    def drop_piece(self):
        self.current_piece["y"] += 1
        if self.check_collision():
            self.current_piece["y"] -= 1
            self.lock_piece()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()
    game = Tetris()
    running = True
    font = pygame.font.SysFont("Arial", 24) 

    drop_timer = 0
    drop_speed = 500  # set drop speed

    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.drop_piece()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()

        drop_timer += clock.get_time()
        if drop_timer > drop_speed:
            game.drop_piece()
            drop_timer = 0

        for y in range(ROWS):
            for x in range(COLS):
                if game.board[y][x]:
                    pygame.draw.rect(screen, game.board[y][x],
                                     (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        shape = game.current_piece["shape"]
        color = game.current_piece["color"]
        x, y = game.current_piece["x"], game.current_piece["y"]
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, color,
                                     ((x + j) * BLOCK_SIZE, (y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        score_text = font.render(f"Score: {game.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30) 

    pygame.quit()

if __name__ == "__main__":
    main()
