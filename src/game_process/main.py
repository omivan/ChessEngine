import chess
import time
import chess.svg
import chess.pgn
from engine import ChessEngine
from eval import get_eval

def board_to_pgn(board):
    game = chess.pgn.Game()
    node = game

    for move in board.move_stack:
        node = node.add_variation(move)

    return game

if __name__ == "__main__":
    board = chess.Board()
    engine = ChessEngine()
    board.push(chess.Move.from_uci('d2d4'))
    board.push(chess.Move.from_uci('d7d6'))
    board.push(chess.Move.from_uci('c2c4'))
    board.push(chess.Move.from_uci('g8f6'))
    board.push(chess.Move.from_uci('b1c3'))
    board.push(chess.Move.from_uci('g7g6'))
    board.push(chess.Move.from_uci('e2e4'))
    board.push(chess.Move.from_uci('f8g7'))
    board.push(chess.Move.from_uci('g1f3'))
    board.push(chess.Move.from_uci('e8g8'))
    board.push(chess.Move.from_uci('f1e2'))
    board.push(chess.Move.from_uci('e7e5'))
    board.push(chess.Move.from_uci('e1g1'))
    board.push(chess.Move.from_uci('b8c6'))
    board.push(chess.Move.from_uci('d4d5'))
    board.push(chess.Move.from_uci('c6e7'))
    board.push(chess.Move.from_uci('f3e1'))
    board.push(chess.Move.from_uci('f6d7'))
    board.push(chess.Move.from_uci('c1e3'))
    board.push(chess.Move.from_uci('f7f5'))
    board.push(chess.Move.from_uci('f2f3'))
    board.push(chess.Move.from_uci('f5f4'))
    print(board.fen())
    # board.push(chess.Move.from_uci('c6e7'))


    # start_time = time.time()
    # best_move1, best_eval1 = engine.get_best_move(board, depth=5)
    # piece1 = board.piece_at(best_move1.from_square).symbol()
    # piece1 = piece1 if piece1 != 'P' else ''
    # board.push(best_move1)
    # end_time = time.time()
    # print(f"{piece1}{best_move1} = "
    #       f"{round(best_eval1, 2)} | {round(end_time - start_time, 2)}")
    # print(engine.node_counter)


    i = 0
    eval = 0
    while True:
        if i == 30:
            break
        i += 1
        start_time = time.time()
        best_move1, best_eval1 = engine.get_best_move(board, depth=4)
        piece1 = board.piece_at(best_move1.from_square).symbol()
        piece1 = piece1 if piece1 != 'P' else ''
        board.push(best_move1)
        eval = get_eval(board)
        if eval in [10000, -10000, 0]:
            print(f"{i}) {piece1}{best_move1} = {round(best_eval1, 2)}")
            break
        best_move2, best_eval2 = engine.get_best_move(board, depth=4)
        piece2 = board.piece_at(best_move2.from_square).symbol().upper()
        piece2 = piece2 if piece2 != 'P' else ''
        board.push(best_move2)
        eval = get_eval(board)
        if eval in [10000, -10000, 0]:
            end_time = time.time()
            print(f"{i}) {piece1}{best_move1} = "
                  f"{round(best_eval1, 2)} | "
                  f"{piece2}{best_move2} = {round(best_eval2, 2)},"
                  f" {round(end_time - start_time, 2)}")
            break
        end_time = time.time()
        print(f"{i}) {piece1}{best_move1} = "
              f"{round(best_eval1, 2)} | "
              f"{piece2}{best_move2} = {round(best_eval2, 2)},"
              f" {round(end_time - start_time, 2)}")

    print("Game is over!")
    print(board.fen())
    print(board_to_pgn(board))

