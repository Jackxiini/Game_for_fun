import pygame
import sys

pygame.init()

CELL_SIZE = 60
ROWS = 10
COLS = 9
SCREEN_WIDTH = COLS * CELL_SIZE  # 540
SCREEN_HEIGHT = ROWS * CELL_SIZE # 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("中国象棋示例")

FONT = pygame.font.SysFont("SimHei", 28)
LARGE_FONT = pygame.font.SysFont("SimHei", 72)

RED_PIECES = {
    'R': '車',
    'N': '馬',
    'B': '相',
    'A': '仕',
    'K': '帅',
    'C': '炮',
    'P': '兵'
}
BLACK_PIECES = {
    'r': '車',
    'n': '馬',
    'b': '象',
    'a': '士',
    'k': '将',
    'c': '炮',
    'p': '卒'
}

initial_board = [
    ['r', 'n', 'b', 'a', 'k', 'a', 'b', 'n', 'r'],
    [None, None, None, None, None, None, None, None, None],
    [None, 'c', None, None, None, None, None, 'c', None],
    ['p', None, 'p', None, 'p', None, 'p', None, 'p'],
    [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None],
    ['P', None, 'P', None, 'P', None, 'P', None, 'P'],
    [None, 'C', None, None, None, None, None, 'C', None],
    [None, None, None, None, None, None, None, None, None],
    ['R', 'N', 'B', 'A', 'K', 'A', 'B', 'N', 'R']
]

board = [row[:] for row in initial_board]

selected_piece = None
selected_pos = None
possible_moves = []
red_turn = True

background_image = pygame.image.load("board_bg.png").convert()

def in_board(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def is_red(piece):
    return piece is not None and piece.isupper()

def is_black(piece):
    return piece is not None and piece.islower()

def same_color(p1, p2):
    if p1 is None or p2 is None:
        return False
    return (is_red(p1) and is_red(p2)) or (is_black(p1) and is_black(p2))

def inside_palace(r, c, red_side):
    if red_side:
        return 7 <= r <= 9 and 3 <= c <= 5
    else:
        return 0 <= r <= 2 and 3 <= c <= 5

def draw_board():
    screen.blit(background_image, (0, 0))
    for col in range(COLS):
        start_pos = (col * CELL_SIZE + CELL_SIZE//2, CELL_SIZE//2)
        end_pos = (col * CELL_SIZE + CELL_SIZE//2, SCREEN_HEIGHT - CELL_SIZE//2)
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)

    for row in range(ROWS):
        start_pos = (CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2)
        end_pos = (SCREEN_WIDTH - CELL_SIZE//2, row * CELL_SIZE + CELL_SIZE//2)
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 1)

    ch_text = FONT.render("楚河", True, (0,0,0))
    hj_text = FONT.render("汉界", True, (0,0,0))
    line4_y = 4 * CELL_SIZE + CELL_SIZE//2
    line5_y = 5 * CELL_SIZE + CELL_SIZE//2
    river_y = (line4_y + line5_y) / 2
    screen.blit(ch_text, (CELL_SIZE * 2 - ch_text.get_width()/2, river_y - ch_text.get_height()/2))
    screen.blit(hj_text, (CELL_SIZE * 5 - hj_text.get_width()/2, river_y - hj_text.get_height()/2))

def draw_pieces():
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece:
                x = c * CELL_SIZE + CELL_SIZE//2
                y = r * CELL_SIZE + CELL_SIZE//2
                pygame.draw.circle(screen, (255, 255, 200), (x, y), CELL_SIZE//2 - 4)
                pygame.draw.circle(screen, (0, 0, 0), (x, y), CELL_SIZE//2 - 4, 2)
                if piece.isupper():
                    text_surface = FONT.render(RED_PIECES[piece], True, (200, 0, 0))
                else:
                    text_surface = FONT.render(BLACK_PIECES[piece], True, (0, 0, 0))
                tw, th = text_surface.get_size()
                screen.blit(text_surface, (x - tw/2, y - th/2))

def draw_highlights():
    for (rr, cc) in possible_moves:
        cell_x = cc * CELL_SIZE
        cell_y = rr * CELL_SIZE
        color = (255,0,0)
        line_len = 10
        line_w = 2
        pygame.draw.line(screen, color, (cell_x, cell_y), (cell_x+line_len, cell_y), line_w)
        pygame.draw.line(screen, color, (cell_x, cell_y), (cell_x, cell_y+line_len), line_w)
        pygame.draw.line(screen, color, (cell_x+CELL_SIZE, cell_y), (cell_x+CELL_SIZE-line_len, cell_y), line_w)
        pygame.draw.line(screen, color, (cell_x+CELL_SIZE, cell_y), (cell_x+CELL_SIZE, cell_y+line_len), line_w)
        pygame.draw.line(screen, color, (cell_x, cell_y+CELL_SIZE), (cell_x+line_len, cell_y+CELL_SIZE), line_w)
        pygame.draw.line(screen, color, (cell_x, cell_y+CELL_SIZE), (cell_x, cell_y+CELL_SIZE-line_len), line_w)
        pygame.draw.line(screen, color, (cell_x+CELL_SIZE, cell_y+CELL_SIZE), (cell_x+CELL_SIZE-line_len, cell_y+CELL_SIZE), line_w)
        pygame.draw.line(screen, color, (cell_x+CELL_SIZE, cell_y+CELL_SIZE), (cell_x+CELL_SIZE, cell_y+CELL_SIZE-line_len), line_w)

    if selected_pos and board[selected_pos[0]][selected_pos[1]]:
        x = selected_pos[1]*CELL_SIZE + CELL_SIZE//2
        y = selected_pos[0]*CELL_SIZE + CELL_SIZE//2
        pygame.draw.circle(screen, (0, 255, 0), (x, y), CELL_SIZE//2 - 2, 2)

def get_cell_from_pos(pos):
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    if in_board(row, col):
        return (row, col)
    return (None, None)

def can_move_R(pos, piece):
    (r, c) = pos
    moves = []
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for dr,dc in directions:
        rr, cc = r, c
        while True:
            rr += dr
            cc += dc
            if not in_board(rr, cc):
                break
            if board[rr][cc]:
                if not same_color(piece, board[rr][cc]):
                    moves.append((rr, cc))
                break
            else:
                moves.append((rr, cc))
    return moves

def can_move_N(pos, piece):
    (r, c) = pos
    moves = []
    potential = [
        (r-2, c-1, (r-1, c)), (r-2, c+1, (r-1, c)),
        (r+2, c-1, (r+1, c)), (r+2, c+1, (r+1, c)),
        (r-1, c-2, (r, c-1)), (r+1, c-2, (r, c-1)),
        (r-1, c+2, (r, c+1)), (r+1, c+2, (r, c+1))
    ]
    for (rr, cc, block) in potential:
        if in_board(rr, cc) and board[block[0]][block[1]] is None:
            if board[rr][cc] is None or not same_color(piece, board[rr][cc]):
                moves.append((rr, cc))
    return moves

def can_move_B(pos, piece):
    (r, c) = pos
    moves = []
    red_side = is_red(piece)
    steps = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    for dr, dc in steps:
        rr, cc = r+dr, c+dc
        mr, mc = r+dr//2, c+dc//2
        if in_board(rr, cc) and board[mr][mc] is None:
            if red_side and rr >= 5:
                if board[rr][cc] is None or not same_color(piece, board[rr][cc]):
                    moves.append((rr, cc))
            if not red_side and rr <= 4:
                if board[rr][cc] is None or not same_color(piece, board[rr][cc]):
                    moves.append((rr, cc))
    return moves

def can_move_A(pos, piece):
    (r, c) = pos
    red_side = is_red(piece)
    moves = []
    steps = [(-1,-1), (-1,1), (1,-1), (1,1)]
    for dr, dc in steps:
        rr, cc = r+dr, c+dc
        if in_board(rr, cc) and inside_palace(rr, cc, red_side):
            if board[rr][cc] is None or not same_color(piece, board[rr][cc]):
                moves.append((rr, cc))
    return moves

def can_move_K(pos, piece):
    (r, c) = pos
    red_side = is_red(piece)
    moves = []
    steps = [(1,0), (-1,0), (0,1), (0,-1)]
    for dr, dc in steps:
        rr, cc = r+dr, c+dc
        if in_board(rr, cc) and inside_palace(rr, cc, red_side):
            if board[rr][cc] is None or not same_color(piece, board[rr][cc]):
                moves.append((rr, cc))
    return moves

def can_move_C(pos, piece):
    (r, c) = pos
    moves = []
    directions = [(1,0),(-1,0),(0,1),(0,-1)]
    for dr, dc in directions:
        rr, cc = r, c
        passed_first_piece = False
        while True:
            rr += dr
            cc += dc
            if not in_board(rr, cc):
                break
            current = board[rr][cc]
            if not passed_first_piece:
                if current is None:
                    moves.append((rr, cc))
                else:
                    passed_first_piece = True
            else:
                if current is not None and not same_color(piece, current):
                    moves.append((rr, cc))
                break
    return moves

def can_move_P(pos, piece):
    (r, c) = pos
    red_side = is_red(piece)
    moves = []
    if red_side:
        forward = (r-1, c)
        if in_board(forward[0], forward[1]):
            if board[forward[0]][forward[1]] is None or not same_color(piece, board[forward[0]][forward[1]]):
                moves.append(forward)
        if r < 5:
            for cc2 in [c-1, c+1]:
                if in_board(r, cc2):
                    if board[r][cc2] is None or not same_color(piece, board[r][cc2]):
                        moves.append((r, cc2))
    else:
        forward = (r+1, c)
        if in_board(forward[0], forward[1]):
            if board[forward[0]][forward[1]] is None or not same_color(piece, board[forward[0]][forward[1]]):
                moves.append(forward)
        if r > 4:
            for cc2 in [c-1, c+1]:
                if in_board(r, cc2):
                    if board[r][cc2] is None or not same_color(piece, board[r][cc2]):
                        moves.append((r, cc2))
    return moves

def get_legal_moves(r, c):
    piece = board[r][c]
    if piece is None:
        return []
    p = piece.upper()
    if p == 'R':
        return can_move_R((r,c), piece)
    elif p == 'N':
        return can_move_N((r,c), piece)
    elif p == 'B':
        return can_move_B((r,c), piece)
    elif p == 'A':
        return can_move_A((r,c), piece)
    elif p == 'K':
        return can_move_K((r,c), piece)
    elif p == 'C':
        return can_move_C((r,c), piece)
    elif p == 'P':
        return can_move_P((r,c), piece)
    return []

def check_winner():
    red_king = False
    black_king = False
    for row in board:
        for p in row:
            if p == 'K':
                red_king = True
            if p == 'k':
                black_king = True
    if not red_king:
        return "黑方胜利！"
    if not black_king:
        return "红方胜利！"
    return None

def show_winner_message(msg):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0,0,0))
    screen.blit(overlay, (0,0))

    text_surface = LARGE_FONT.render(msg, True, (255, 255, 0))
    tw, th = text_surface.get_size()
    screen.blit(text_surface, ((SCREEN_WIDTH - tw)//2, (SCREEN_HEIGHT - th)//2))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main():
    global selected_piece, selected_pos, possible_moves, red_turn
    clock = pygame.time.Clock()
    running = True
    print("红方先走。")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                rr, cc = get_cell_from_pos(mouse_pos)
                if rr is not None and cc is not None:
                    if selected_piece is None:
                        piece = board[rr][cc]
                        if piece and ((red_turn and is_red(piece)) or (not red_turn and is_black(piece))):
                            selected_piece = piece
                            selected_pos = (rr, cc)
                            possible_moves = get_legal_moves(rr, cc)
                    else:
                        if (rr, cc) in possible_moves:
                            board[selected_pos[0]][selected_pos[1]] = None
                            board[rr][cc] = selected_piece
                            selected_piece = None
                            selected_pos = None
                            possible_moves = []

                            winner = check_winner()
                            if winner:
                                draw_board()
                                draw_pieces()
                                draw_highlights()
                                pygame.display.flip()
                                show_winner_message(winner)
                                running = False
                            else:
                                red_turn = not red_turn
                                print("轮到{}方走".format("红" if red_turn else "黑"))
                        else:
                            piece = board[rr][cc]
                            if piece and ((red_turn and is_red(piece)) or (not red_turn and is_black(piece))):
                                selected_piece = piece
                                selected_pos = (rr, cc)
                                possible_moves = get_legal_moves(rr, cc)
                            else:
                                selected_piece = None
                                selected_pos = None
                                possible_moves = []

        draw_board()
        draw_pieces()
        draw_highlights()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()



