import random
from typing import List


win_combinations = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def cell_idx(x, y) -> int:
    return (x - 1) + 3 * (3 - y)


def free_cell_indices(cells) -> List[int]:
    return [i for i, tile in enumerate(cells) if tile not in ('X', 'O')]


def print_cells(cells):
    print('---------')
    for start in (0, 3, 6):
        print('|', ' '.join(cells[start:start + 3]), '|')
    print('---------')


def does_win(cells, tile):
    return any(all(cells[i] == tile for i in indices) for indices in win_combinations)


def check_cells(cells) -> str:
    if does_win(cells, 'X'):
        return 'X wins'
    if does_win(cells, 'O'):
        return 'O wins'
    if not free_cell_indices(cells):
        return 'Draw'
    return 'Game not finished'


def tic_tac_toe(player1, player2):
    cells = [' '] * 9
    print_cells(cells)

    player1_tile, player2_tile = 'X', 'O'

    while True:
        idx = player1(cells, tile=player1_tile, opponent_tile=player2_tile)
        cells[idx] = player1_tile

        print_cells(cells)
        game_result = check_cells(cells)
        if game_result != 'Game not finished':
            break

        idx = player2(cells, tile=player2_tile, opponent_tile=player1_tile)
        cells[idx] = player2_tile

        print_cells(cells)
        game_result = check_cells(cells)
        if game_result != 'Game not finished':
            break

    print(game_result)


def user_next_move(cells, **_) -> int:
    while True:
        try:
            x, y = tuple(map(int, input('Enter the coordinates: ').split()))
        except ValueError:
            print('You should enter numbers!')
            continue

        if x < 1 or x > 3 or y < 1 or y > 3:
            print('Coordinates should be from 1 to 3!')
            continue

        idx = cell_idx(x, y)
        if idx not in free_cell_indices(cells):
            print('This cell is occupied! Choose another one!')
            continue
        return idx


def easy_bot_next_move(cells, **_) -> int:
    print('Making move level "easy"')
    return random.choice(free_cell_indices(cells))


def medium_bot_next_move(cells, tile, **_) -> int:
    print('Making move level "medium"')
    free_cells = free_cell_indices(cells)

    # find next winning move
    for comb in win_combinations:
        for i1, i2, i3 in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
            if cells[comb[i1]] == tile and cells[comb[i2]] == tile and comb[i3] in free_cells:
                return comb[i3]

    # find opponent's next winning move
    for comb in win_combinations:
        for i1, i2, i3 in ((0, 1, 2), (2, 0, 1), (1, 2, 0)):
            if cells[comb[i1]] == cells[comb[i2]] and comb[i3] in free_cells:
                return comb[i3]

    # make random move
    return random.choice(free_cells)


def minimax_move(cells, current_player, player1, player2) -> dict:
    """Finds the next best next move for player1 using minimax algorithm.
       Returned move objects contains 'score' and the move 'index' (if any) keys.
    """
    if does_win(cells, player1):
        return {'score': 10}
    if does_win(cells, player2):
        return {'score': -10}

    free_cells = free_cell_indices(cells)
    if not free_cells:
        return {'score': 0}

    moves = []
    for idx in free_cells:
        move = {'index': idx}
        cells[idx] = current_player

        if current_player == player1:
            move['score'] = minimax_move(cells, player2, player1, player2)['score']
        else:
            move['score'] = minimax_move(cells, player1, player1, player2)['score']

        # reset the spot to empty
        cells[idx] = ' '
        moves.append(move)

    if current_player == player1:
        return min(moves, key=lambda m: m['score'])
    else:
        return max(moves, key=lambda m: m['score'])


def hard_bot_next_move(cells, tile, opponent_tile, **_) -> int:
    print('Making move level "hard"')
    return minimax_move(cells, tile, tile, opponent_tile)['index']


def main():
    def new_player(kind: str):
        if kind == 'user':
            return user_next_move
        elif kind == 'easy':
            return easy_bot_next_move
        elif kind == 'medium':
            return medium_bot_next_move
        elif kind == 'hard':
            return hard_bot_next_move
        return None

    while True:
        cmd = input().lower().split()
        if len(cmd) == 1 and cmd[0] == 'exit':
            break
        elif len(cmd) == 3 and cmd[0] == 'start':
            player1, player2 = new_player(cmd[1]), new_player(cmd[2])
            if not player1 or not player2:
                print('Bad parameters')
                continue
            tic_tac_toe(player1, player2)
        else:
            print('Invalid command')


if __name__ == '__main__':
    main()
