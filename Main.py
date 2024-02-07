"""
main driver file.
Responsible for handling user input and displaying current gamestate
"""

import chess
import pygame as p
import numpy as np
import time

p.init()
BOARD_WIDTH = BOARD_HEIGHT = 512  # size of our board
MOVE_LOG_PANEL_WIDTH = 256
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # Dimension of our chess board is 8x8
SQ_SIZE = BOARD_WIDTH // DIMENSION  # size of each square
MAX_FPS = 30

# initialize global directory of images .This will be called exactly once in the main
IMAGES = {
    'p': p.transform.scale(p.image.load('images/bp.png'), (SQ_SIZE, SQ_SIZE)),
    'n': p.transform.scale(p.image.load('images/bN.png'), (SQ_SIZE, SQ_SIZE)),
    'b': p.transform.scale(p.image.load('images/bB.png'), (SQ_SIZE, SQ_SIZE)),
    'r': p.transform.scale(p.image.load('images/bR.png'), (SQ_SIZE, SQ_SIZE)),
    'q': p.transform.scale(p.image.load('images/bQ.png'), (SQ_SIZE, SQ_SIZE)),
    'k': p.transform.scale(p.image.load('images/bK.png'), (SQ_SIZE, SQ_SIZE)),
    'P': p.transform.scale(p.image.load('images/wp.png'), (SQ_SIZE, SQ_SIZE)),
    'N': p.transform.scale(p.image.load('images/wN.png'), (SQ_SIZE, SQ_SIZE)),
    'B': p.transform.scale(p.image.load('images/wB.png'), (SQ_SIZE, SQ_SIZE)),
    'R': p.transform.scale(p.image.load('images/wR.png'), (SQ_SIZE, SQ_SIZE)),
    'Q': p.transform.scale(p.image.load('images/wQ.png'), (SQ_SIZE, SQ_SIZE)),
    'K': p.transform.scale(p.image.load('images/wK.png'), (SQ_SIZE, SQ_SIZE)),
}

colors = [(240, 217, 181), (181, 136, 99)]  # light , dark squares

PIECES = ['p', 'r', 'n', 'b', 'k', 'q', 'P', 'R', 'N', 'B', 'K', 'Q']


def main():
    # main driver function , handles inputs and graphics update
    sqSelected = ()
    Indices = []  # keeps track of player clicks

    screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))  # set up the screen
    p.display.set_caption("Chess")
    screen.fill(p.Color("white"))

    board = chess.Board()

    drawGameState(screen, board, sqSelected)
    p.display.flip()  # Update the display
    time.sleep(1)
    running = True
    while running:

        if board.is_checkmate():  # restart the game, once check mate or stalemate
            gameOver = True
        elif board.is_stalemate():
            gameOver = True

        for e in p.event.get():
            if e.type == p.QUIT:  # exits the game
                running = False
                break
            elif e.type == p.MOUSEBUTTONUP:
                location = p.mouse.get_pos()  # x, y coordinate of mouse click
                col = (DIMENSION - 1) - (location[1] // SQ_SIZE)
                row = (location[0] // SQ_SIZE)
                index = chess_index_from_row_col(row, col)
                Indices.append(index)
                sqSelected = (row, col)
                # determining which square user clicked

                if board.piece_at(index) is None and len(Indices) == 1:
                    Indices.append(chess_index_from_row_col(row, col))

                if len(Indices) == 2:
                    # once 2 clicks are made to move the piece, move the piece
                    move = chess.Move(Indices[0], Indices[1])
                    if move in board.legal_moves:
                        # If the move is valid, make the move
                        board.push(move)
                    Indices = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    # if key entered is "z", undo moves
                    if board.move_stack:
                        board.pop()

                if e.key == p.K_r:
                    # if key entered is "r", reset board
                    board = chess.Board()
                    Indices = []

            drawGameState(screen, board, sqSelected)  # draw the board
            p.display.flip()


def chess_index_from_row_col(row, col):
    """
    Convert row and column values to chessboard index.

    Args:
    - row (int): Row value (0-7).
    - col (int): Column value (0-7).

    Returns:
    - index (int): Chessboard index (0-63).
    """
    # Convert row and column to chessboard index
    index = col * 8 + row

    return index


def row_col_from_chess_index(index):
    """
    Convert chessboard index to row and column values.

    Args:
    - index (int): Chessboard index (0-63).

    Returns:
    - row (int): Row value (0-7).
    - col (int): Column value (0-7).
    """
    # Calculate row and column from chessboard index
    row = index % 8
    col = index // 8

    return row, col


def drawGameState(screen, board, sqSelected=None):
    # responsible for all graphics with current game state

    drawBoard(screen)


def drawBoard(screen):
    # Draw the board, top left cell is always white

    global colors

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            # every other cell has same color, i.e. sum of row and column will be even/ odd for each color
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()
