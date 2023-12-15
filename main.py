import chess
import numpy as np
from eval import get_eval

def minimax(board, depth, maximizing_player, alpha, beta):
    multiply_coff = -1 if board.turn == chess.WHITE else +1
    # print(multiply_coff)
    if depth == 0 or board.is_game_over():
        return multiply_coff * get_eval(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False, alpha, beta)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True, alpha, beta)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    legal_moves = list(board.legal_moves)
    best_move = None
    best_eval = float('-inf')

    for move in legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, False, float('-inf'), float('inf'))
        board.pop()

        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move


if __name__ == "__main__":
    board = chess.Board()
    for i in range(20):
        best_move1 = find_best_move(board, depth=3)
        board.push(best_move1)
        best_move2 = find_best_move(board, depth=3)
        board.push(best_move2)
        print(f"{i+1}) {best_move1} {best_move2}")

    # best_move = find_best_move(board, depth=3)

    # board.push(chess.Move.from_uci('e2e3'))
    # board.push(chess.Move.from_uci('d7d6'))
    # board.push(chess.Move.from_uci('f1e2'))
    # board.push(chess.Move.from_uci('c8d7'))
    # board.push(chess.Move.from_uci('e1f1'))
    # board.push(chess.Move.from_uci('d8d5'))
    # evaluation = get_eval(board)
    # print("Board Evaluation:", round(evaluation, 2))
