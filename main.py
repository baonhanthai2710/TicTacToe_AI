import sys
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Screen Dimensions
WIDTH = 700
HEIGHT = 800  # Increased height for larger screen and banners
PADDING = 100  # Space for banners at the top

# Board Settings
BOARD_ROWS = 3
BOARD_COLS = 3
LINE_WIDTH = 5
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

# Fonts for banners and messages
pygame.font.init()
title_font = pygame.font.Font(None, 50)  # Font for title banner
subtitle_font = pygame.font.Font(None, 36)  # Font for subtitle banner
message_font = pygame.font.Font(None, 60)  # Font for endgame messages

# Text for banners
title_text = title_font.render("Tic Tac Toe - AI Minimax Algorithm", True, WHITE)
subtitle_text = subtitle_font.render("Gr7 - Nhan/Trung/Dinh Project", True, WHITE)

# Game Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))


def draw_banners():
    """Draws the banners at the top of the screen."""
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 20))
    screen.blit(subtitle_text, ((WIDTH - subtitle_text.get_width()) // 2, 60))


def draw_lines(color=WHITE):
    """Draws the grid lines on the board."""
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, PADDING + SQUARE_SIZE * i), (WIDTH, PADDING + SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, PADDING), (SQUARE_SIZE * i, HEIGHT - (HEIGHT - PADDING - WIDTH)), LINE_WIDTH)


def draw_figures(color=WHITE):
    """Draws X and O on the board."""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4),
                                 (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, PADDING + row * SQUARE_SIZE + SQUARE_SIZE // 4),
                                 CROSS_WIDTH)


def display_message(message, color=WHITE):
    """Displays a message at the center of the screen."""
    text = message_font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, PADDING + WIDTH // 2))
    screen.blit(text, text_rect)


def mark_square(row, col, player):
    """Marks a square with the player's move."""
    board[row][col] = player


def available_square(row, col):
    """Checks if a square is available."""
    return board[row][col] == 0


def is_board_full():
    """Checks if the board is full."""
    return not (board == 0).any()


def check_win(player):
    """Checks if the player has won."""
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False


def minimax(minimax_board, depth, is_maximizing):
    """Minimax algorithm for AI."""
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


def best_move():
    """Calculates the best move for the AI."""
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def restart_game():
    """Restarts the game."""
    screen.fill(BLACK)
    draw_banners()
    draw_lines()
    board.fill(0)

def display_end_screen(message, color=WHITE):
    """Displays the endgame message with a background and a 'Play Again' button."""
    # Background overlay
    overlay_rect = pygame.Rect(50, PADDING + 50, WIDTH - 100, WIDTH // 2)
    pygame.draw.rect(screen, BLACK, overlay_rect)
    pygame.draw.rect(screen, WHITE, overlay_rect, 5)

    # Display message
    text = message_font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, PADDING + 100))
    screen.blit(text, text_rect)

    # Draw "Play Again" button
    button_rect = pygame.Rect(WIDTH // 2 - 75, PADDING + 150, 150, 50)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 3)

    # Button text
    button_text = subtitle_font.render("Play Again", True, BLACK)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

    return button_rect

def draw_start_menu():
    """Draws the start menu with title, subtitle, and buttons."""
    # Clear the screen
    screen.fill(BLACK)

    # Draw titles
    screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, 100))
    screen.blit(subtitle_text, ((WIDTH - subtitle_text.get_width()) // 2, 160))

    # Draw buttons
    ai_button_rect = pygame.Rect(WIDTH // 2 - 100, 250, 200, 50)
    player_button_rect = pygame.Rect(WIDTH // 2 - 100, 350, 200, 50)

    pygame.draw.rect(screen, GRAY, ai_button_rect)
    pygame.draw.rect(screen, GRAY, player_button_rect)
    pygame.draw.rect(screen, WHITE, ai_button_rect, 3)
    pygame.draw.rect(screen, WHITE, player_button_rect, 3)

    # Button text
    ai_text = subtitle_font.render("AI vs Player", True, BLACK)
    player_text = subtitle_font.render("Player vs Player", True, BLACK)

    screen.blit(ai_text, ai_text.get_rect(center=ai_button_rect.center))
    screen.blit(player_text, player_text.get_rect(center=player_button_rect.center))

    return ai_button_rect, player_button_rect

def handle_start_menu_click(ai_button, player_button, event):
    """Handles clicks on the start menu buttons."""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if ai_button.collidepoint(event.pos):
            return "AI_vs_Player"
        elif player_button.collidepoint(event.pos):
            return "Player_vs_Player"
    return None


# Initial Setup
draw_banners()
draw_lines()

player = 1
game_over = False
winner_message = ""

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = (event.pos[1] - PADDING) // SQUARE_SIZE
            if 0 <= mouseY < BOARD_ROWS and available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                    winner_message = "Player Wins!" if player == 1 else "AI Wins!"
                player = 3 - player  # Switch player

                if not game_over and player == 2:  # AI's turn
                    if best_move():
                        if check_win(2):
                            game_over = True
                            winner_message = "AI Wins!"
                        player = 3 - player

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1
                winner_message = ""

    screen.fill(BLACK)
    draw_banners()
    draw_lines()
    draw_figures()

    if game_over:
        if is_board_full() and not winner_message:
            winner_message = "It's a Draw!"
        button_rect = display_end_screen(winner_message, GREEN if winner_message == "Player Wins!" else RED)

        # Check for button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                restart_game()
                game_over = False
                player = 1
                winner_message = ""


    pygame.display.update()
