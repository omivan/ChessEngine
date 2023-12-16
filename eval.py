import chess
import numpy as np


def get_eval(board):
    if board.is_game_over():
        color = 1 if board.turn == chess.WHITE else -1
        if board.is_checkmate():
            return -color * 10000
        elif (board.is_stalemate()
              or board.is_seventyfive_moves() or
              board.is_fivefold_repetition() or
              board.is_insufficient_material()):
            return 0

    piece_values = {
        chess.QUEEN: 9,
        chess.ROOK: 5,
        chess.BISHOP: 3,
        chess.KNIGHT: 3,
        chess.PAWN: 1
    }

    pawn_position_values = np.array([
         8, 8, 8, 8, 8, 8, 8, 8,
         8, 8, 8, 9, 9, 8, 8, 8,
         5, 6, 7, 8, 8, 7, 6, 5,
         2, 3, 6, 7, 8, 6, 3, 2,
         1, 1, 5, 6, 6, 3, 1, 1,
         1, 1, 2, 3, 3, 2, 1, 1,
         1, 1, 1, 0, 0, 1, 1, 1,
         0, 0, 0, 0, 0, 0, 0, 0
    ])
    queen_position_values = np.array([
         1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 3, 1, 1, 1, 1,
         1, 4, 1, 1, 1, 2, 1, 1,
         1, 1, 4, 4, 3, 1, 1, 1,
         1, 1, 1, 2, 1, 1, 1, 1
    ])
    knight_position_values = np.array([
        1, 3, 2, 2, 2, 2, 3, 1,
        2, 3, 3, 3, 3, 3, 3, 2,
        2, 3, 4, 4, 4, 4, 3, 2,
        2, 3, 4, 5, 5, 4, 3, 2,
        2, 3, 4, 5, 5, 4, 3, 2,
        2, 3, 5, 4, 4, 5, 3, 2,
        2, 3, 3, 3, 3, 3, 3, 2,
        1, 3, 2, 2, 2, 2, 3, 1
    ])
    bishop_position_values = np.array([
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 3,
        1, 3, 1, 1, 1, 1, 3, 1,
        3, 2, 5, 1, 1, 5, 2, 3,
        2, 4, 2, 2, 2, 2, 4, 2,
        2, 5, 4, 2, 3, 2, 5, 4,
        1, 1, 1, 1, 1, 2, 1, 1
    ])

    rook_position_values = np.array([
        4, 4, 4, 4, 4, 4, 4, 5,
        5, 5, 5, 5, 5, 5, 5, 5,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        2, 1, 1, 1, 1, 1, 1, 2,
        1, 1, 2, 3, 3, 2, 1, 1,
        2, 1, 4, 5, 5, 4, 1, 2
    ])

    king_position_values = np.array([
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 3, 2, 1, 1, 1, 1, 3,
        4, 6, 5, 3, 5, 2, 8, 5
    ])
    piece_position_coffs = {
        chess.PAWN: 0.05,
        chess.ROOK: 0.05,
        chess.KNIGHT: 0.1,
        chess.BISHOP: 0.1,
        chess.KING: 0.2,
        chess.QUEEN: 0.05
    }
    piece_position_values = {
        chess.PAWN: pawn_position_values,
        chess.ROOK: rook_position_values,
        chess.KNIGHT: knight_position_values,
        chess.BISHOP: bishop_position_values,
        chess.KING: king_position_values,
        chess.QUEEN: queen_position_values
    }
    total_evaluation = 0
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        color_multiplier = 1 if piece.color == chess.WHITE else -1
        piece_value = piece_values.get(piece.piece_type, 0)
        total_evaluation += color_multiplier * piece_value

        if piece.piece_type in piece_position_values:
            position_matrix = piece_position_values[piece.piece_type]

            index = (7 - square // 8) * 8 + square % 8 \
                if piece.color == chess.WHITE else (square // 8) * 8 + square % 8

            total_evaluation += (
                    color_multiplier *
                    piece_position_coffs[piece.piece_type] *
                    position_matrix[index])



    return total_evaluation
