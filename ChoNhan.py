import sys
import pygame
import numpy as np

# Khởi tạo
pygame.init()

# Định nghĩa màu sắc
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Kích thước màn hình
WIDTH = 700
HEIGHT = 800
PADDING = 100

# Các biến toàn cục
BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 5
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Khởi tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(WHITE)

# Font tiêu đề và thông báo
pygame.font.init()
title_font = pygame.font.Font('freesansbold.ttf', 40)
subtitle_font = pygame.font.Font(None, 36)
message_font = pygame.font.Font(None, 60)

# Tên game và nhóm
title_text = title_font.render("Tic Tac Toe - AI Minimax Algorithm", True, BLACK)
subtitle_text = subtitle_font.render("Gr7 - Nhan/Trung/Dinh Project", True, BLACK)

# Vẽ tiêu đề
def draw_banners():
    screen.fill(WHITE)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 20))
    screen.blit(subtitle_text, ((WIDTH - subtitle_text.get_width()) // 2, 60))
    separator_y = 60 + subtitle_text.get_height() + 10
    pygame.draw.line(screen, BLACK, (0, separator_y), (WIDTH, separator_y), 5)

# Cập nhật kích thước bảng
def update_board_size(size):
    global BOARD_ROWS, BOARD_COLS, SQUARE_SIZE, board
    BOARD_ROWS = size
    BOARD_COLS = size
    SQUARE_SIZE = WIDTH // BOARD_COLS
    board = np.zeros((BOARD_ROWS, BOARD_COLS))

# Vẽ các đường chia ô
def draw_lines(color=BLACK):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, PADDING + SQUARE_SIZE * i), (WIDTH, PADDING + SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, PADDING), (SQUARE_SIZE * i, HEIGHT - (HEIGHT - PADDING - WIDTH)), LINE_WIDTH)

# Vẽ các lượt chơi
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # X
                pygame.draw.line(screen, BLUE,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, BLUE,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
            elif board[row][col] == 2:  # O
                pygame.draw.circle(screen, RED,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Đánh dấu ô
def mark_square(row, col, player):
    board[row][col] = player

# Kiểm tra ô còn trống
def available_square(row, col):
    return board[row][col] == 0

# Kiểm tra bảng có còn ô trống
def is_board_full():
    return not (board == 0).any()

# Kiểm tra thắng
def check_win(player):
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return True

    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return True

    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return True

    if all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        return True

    return False

# Thuật toán minimax
def minimax(minimax_board, depth, is_maximizing):
    if check_win(2):
        return float('inf')
    elif check_win(1):
        return float('-inf')
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

# Tìm nước đi tốt nhất
def best_move(player):
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = player
                score = minimax(board, 0, False if player == 2 else True)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], player)
        return True
    return False

# Hiển thị menu chọn chế độ chơi
def draw_game_mode_selection():
    draw_banners()
    title_text = subtitle_font.render("Choose Game Mode", True, BLACK)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, PADDING))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 200, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 200, 400, 60), 5)
    screen.blit(subtitle_font.render("Player vs Player", True, BLACK), (220, 210))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 280, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 280, 400, 60), 5)
    screen.blit(subtitle_font.render("Player vs AI", True, BLACK), (270, 290))

# Hiển thị menu chọn kích thước
def draw_size_selection():
    draw_banners()
    title_text = subtitle_font.render("Choose Board Size", True, BLACK)
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, PADDING))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 200, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 200, 400, 60), 5)
    screen.blit(subtitle_font.render("3x3", True, BLACK), (320, 210))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 280, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 280, 400, 60), 5)
    screen.blit(subtitle_font.render("4x4", True, BLACK), (320, 290))

    pygame.draw.rect(screen, GRAY, pygame.Rect(150, 360, 400, 60))
    pygame.draw.rect(screen, WHITE, pygame.Rect(150, 360, 400, 60), 5)
    screen.blit(subtitle_font.render("5x5", True, BLACK), (320, 370))

# Main game loop
game_mode = None
player = 1
game_over = False
winner_message = ""
size_chosen = False

while True:
    if game_mode is None:
        draw_game_mode_selection()
    elif not size_chosen:
        draw_size_selection()
    else:
        draw_banners()
        draw_lines()
        draw_figures()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_mode is None and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 150 < x < 550 and 200 < y < 260:
                game_mode = "PvP"
            elif 150 < x < 550 and 280 < y < 340:
                game_mode = "PvAI"

        elif not size_chosen and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 150 < x < 550 and 200 < y < 260:
                update_board_size(3)
                size_chosen = True
            elif 150 < x < 550 and 280 < y < 340:
                update_board_size(4)
                size_chosen = True
            elif 150 < x < 550 and 360 < y < 420:
                update_board_size(5)
                size_chosen = True

        elif size_chosen and not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            clicked_row = (mouse_y - PADDING) // SQUARE_SIZE
            clicked_col = mouse_x // SQUARE_SIZE

            if game_mode == "PvP" and available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                    winner_message = f"Player {player} wins!"
                player = 1 if player == 2 else 2

            elif game_mode == "PvAI" and player == 1 and available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                    winner_message = "Player X wins!"
                player = 2

        if game_mode == "PvAI" and player == 2 and not game_over:
            best_move(player)
            if check_win(player):
                game_over = True
                winner_message = "Player O wins!"
            player = 1

    if game_over:
        pygame.time.wait(1000)
        screen.fill(WHITE)
        winner_text = message_font.render(winner_message, True, GREEN)
        screen.blit(winner_text, ((WIDTH - winner_text.get_width()) // 2, HEIGHT // 2))

    pygame.display.update()
