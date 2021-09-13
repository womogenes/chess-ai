import chess
import random
from functools import lru_cache
import time
from tables import PAWNOPENINGTABLE, KNIGHTTABLE, BISHOPTABLE, ROOKTABLE, QUEENTABLE, KINGMIDDLETABLE

value = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

tables = {
    chess.PAWN: PAWNOPENINGTABLE,
    chess.KNIGHT: KNIGHTTABLE,
    chess.BISHOP: BISHOPTABLE,
    chess.ROOK: ROOKTABLE,
    chess.QUEEN: QUEENTABLE,
    chess.KING: KINGMIDDLETABLE
}


def flip(x):
    """
    Weird formula to flip the board around
    """
    return 8 * (7 - x // 8) + x % 8


def evaluate(board):
    outcome = board.outcome()
    if outcome:
        if outcome.result() == "1-0":
            return 99
        elif outcome.result() == "0-1":
            return -99
        return 0

    valuation = 0
    for piece in board.piece_map().values():
        valuation += value[piece.piece_type] * (piece.color - 0.5) * 2

    # Add some positioning
    for square, piece in board.piece_map().items():
        if piece.color:
            #print(square, piece, tables[piece.piece_type][square])
            valuation += tables[piece.piece_type][square] * \
                0.1 * 1
        else:
            #print(flip(square), piece, tables[piece.piece_type][flip(square)])
            valuation += tables[piece.piece_type][flip(
                square)] * 0.1 * -1

    return valuation


def minimax(board, depth):
    """
    Evaluate the best move using minimax up to depth.
    """
    if not bool(board.legal_moves):
        return None

    if depth == 0:
        return random.choice(list(board.legal_moves))

    best_move = None
    if board.turn:
        best_val = -9999
    else:
        best_val = 9999

    possible_moves = list(board.legal_moves)
    random.shuffle(possible_moves)
    for move in board.legal_moves:
        board_copy = board.copy(stack=False)
        board_copy.push(move)

        # Compute the outcome
        next_move = minimax(board_copy, depth - 1)

        if next_move == None:
            if board_copy.outcome().winner == board.turn:
                return move
            continue

        board_copy.push(next_move)
        move_value = evaluate(board_copy)

        if board.turn:
            if move_value >= best_val:
                best_val = move_value
                best_move = move
                # print(move_value)

        else:
            if move_value <= best_val:
                best_val = move_value
                best_move = move
                # print(move_value)

    return best_move


board = chess.Board()

while True:
    print(board)
    mover = 'white' if board.turn else 'black'
    print(
        f"Turn: {mover} \t Evaluation: {evaluate(board)}")
    if board.outcome():
        print(board.outcome())
        break

    input()
    start_time = time.time()
    move = minimax(board, 3)
    #print(f"Done in {time.time() - start_time} seconds.")
    print(f"{board.san(move)} was played by {mover}")
    board.push(move)
