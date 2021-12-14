import fileinput
from bisect import bisect
from collections import defaultdict

game_size = 5


def bingo():
    f = fileinput.input()
    board = []
    boards = []

    numbers = list(map(int, filter(None, next(f).strip().split(','))))
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            if not board:
                continue

            boards.append(board)
            board = []
        else:
            row = list(map(int, filter(None, line.split(' '))))
            board.append(row)

    if board:
        boards.append(board)

    return {
        'boards': boards,
        'numbers': numbers,
    }


def index(boards):
    return sorted([
        (xy, board_i, row_i, col_i)
        for board_i, board in enumerate(boards)
        for row_i, row in enumerate(board)
        for col_i, xy in enumerate(row)
    ])


def score(numbers, board, success_number):
    marked = set(numbers[:numbers.index(success_number) + 1])
    unmarked_sum = sum(xy for row in board for xy in row if xy not in marked)
    return success_number * unmarked_sum


def find_success_board(numbers, board_index, is_success):
    # {board_number: {column: {column_number: drawn_count}, row: {row_number: drawn_count}}}
    drawn = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  
    success_boards = set()

    success_number = None
    success_board = None
    for number in numbers:
        if is_success(success_boards):
            break

        i_left = bisect(board_index, (number, 0, 0, 0))
        for i in range(i_left, len(board_index)):
            xy, board_number, i_col, i_row = board_index[i]
            if xy != number:
                break

            if board_number in success_boards:
                continue

            board = drawn[board_number]
            board['row'][i_row] += 1
            board['col'][i_col] += 1

            if board['row'][i_row] == game_size or board['col'][i_col] == game_size:
                success_number = number
                success_board = board_number
                success_boards.add(board_number)
    return {'board_number': success_board, 'success_number': success_number}


def solve(numbers, boards):
    board_index = index(boards)
    first_success = find_success_board(
        numbers,
        board_index,
        lambda xs: len(xs) == 1,
    )
    print(score(numbers, boards[first_success['board_number']], first_success['success_number']))

    last_success = find_success_board(
        numbers,
        board_index,
        lambda xs: len(xs) == len(boards),
    )
    print(score(numbers, boards[last_success['board_number']], last_success['success_number']))

solve(**bingo())

