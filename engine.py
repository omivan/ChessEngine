import chess
from eval import get_eval
import random


class ChessEngine:
    def __init__(self):
        self.node_counter = 0

    def sort_moves(self, legal_moves, board):
        captures = [move for move in legal_moves if board.is_capture(move)]
        checks = [move for move in legal_moves if board.gives_check(move)]
        others = [move for move in legal_moves if move not in captures + checks]

        sorted_moves = captures + checks + others
        return sorted_moves

    # def null_move_pruning(self, board, depth, alpha, beta, color):
    #     if depth >= 3:
    #         board.push(chess.Move.null())
    #         null_move_value = -self.negamax(board, depth - 3, -beta, -beta + 1, -color)
    #         board.pop()
    #         if null_move_value >= beta:
    #             return beta
    #     return None

    # def futility_pruning(self, eval_score, beta):
    #     futility_margin = 100
    #     return eval_score + futility_margin < beta

    def negamax(self, board, depth, alpha, beta, color):
        self.node_counter += 1


        if depth == 0 or board.is_game_over():
            return color * get_eval(board)

        # null_move_prune = self.null_move_pruning(board, depth, alpha, beta, color)
        # if null_move_prune is not None:
        #     return null_move_prune

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        legal_moves = self.sort_moves(legal_moves, board)
        max_value = float('-inf')

        for move in legal_moves:
            board.push(move)
            value = -self.negamax(board, depth - 1, -beta, -alpha, -color)
            board.pop()

            if value > max_value:
                max_value = value

            if max_value > alpha:
                alpha = max_value

            # if alpha >= beta or self.futility_pruning(max_value, beta):
            #     break
            if alpha >= beta:
                break

        return max_value

    def get_best_move(self, board, depth, alpha=float('-inf'), beta=float('inf')):
        best_move = None
        max_eval = float('-inf')

        legal_moves = list(board.legal_moves)
        random.shuffle(legal_moves)
        legal_moves = self.sort_moves(legal_moves, board)

        for move in legal_moves:
            board.push(move)
            eval_score = -self.negamax(board, depth - 1, -beta, -alpha,
                                       1 if board.turn == chess.WHITE else -1)
            board.pop()
            if eval_score == 10000:
                print("ok")
                return move, eval_score
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            if eval_score >= alpha:
                alpha = eval_score

            if alpha >= beta:
                break

        return best_move, max_eval
