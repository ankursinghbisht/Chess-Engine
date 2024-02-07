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


