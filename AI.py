import random
import numpy as np
import tensorflow as tf
import chess

MODEL = tf.keras.models.load_model("D:\Repos\Chess-Engine\model.h5", compile=False)

board = chess.Board()
pieceScore = {"K": 0, "Q": 9, "R": 5, "N": 3, "B": 3, "p": 1}
CHECKMATE = 10000
STALEMATE = 0
DEPTH = 1
nextMove = None  # set a global variable to store the best possible move in current game state

squares_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
Boards = []
Evals = None


def square_to_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), squares_index[letter[0]]


def split_dims(board):
    board3d = np.zeros((14, 8, 8), dtype=np.int8)  # 3d representation of board

    # add pieces to board representation
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1

        for square in board.pieces(piece, chess.BLACK):
            idx = np.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

    # adding valid moves
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[13][i][j] = 1
    board.turn = aux

    return board3d


def findBestMove(board):
    # helper method to make first recursive call
    global nextMove
    findMove(board, DEPTH, -CHECKMATE, CHECKMATE, 1 if board.turn == chess.WHITE else -1)
    return nextMove


def findMove(board, depth, alpha, beta, turnMultiplier):
    # NegaMax with Alpha Beta Pruning
    global nextMove
    global Evals
    if depth == 0:
        Boards = []
        validMoves = list(board.legal_moves)
        for move in validMoves:
            board.push(move)
            Boards.append(split_dims(board))
            board.pop()
        evals = evaluate_boards(Boards, turnMultiplier)
        return evals

    validMoves = list(board.legal_moves)
    maxScore = -CHECKMATE
    for move in validMoves:
        board.push(move)
        score = -findMove(board, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        board.pop()

        if maxScore > alpha:  # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def evaluate_boards(Boards, turnMultiplier):
    x_input = np.array(Boards)
    x_input = tf.convert_to_tensor(x_input, dtype=tf.float32)
    y = MODEL(x_input) * turnMultiplier
    return np.max(y)


def evaluate_board(board):
    x = split_dims(board)
    x = np.expand_dims(x, axis=0)
    y = MODEL(x)
    y = np.squeeze(y) * 10000
    return y
