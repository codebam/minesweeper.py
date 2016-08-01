#!/usr/bin/env python3

"""
Text based Minesweeper
Made by Sean Behan
Licenced with GPLv3
"""

from random import randint

INVALID_NUM = "Invalid number, try again..."
WIN = "Congradulations, You won!"
LOSE = "Good try! You lose"
TOOLS = ('1. Reveal', '2. Flag')


def check_mine(x, y, field):
    try:
        if field[x][y]['is_a_mine']:
            return 1
    except IndexError:
        pass
    return 0


def init_field(rows, columns):  # this is the first time through, just generates an empty field
    field = [[{} for x in range(rows)] for y in range(columns)]  # generates empty field
    for x in range(rows):
        for y in range(columns):
            field[x][y] = {
                    'is_a_mine': False,
                    'surrounding_mines': 0,
                    'display':'?',
            }
    return field


def add_mines(rows, columns, field, mines):
    mines_count = 0
    while mines_count < mines:
        for x in range(rows):
            if mines_count < mines:
                for y in range(columns):
                    if mines_count < mines:
                        mine_random = randint(1, 8)
                        if mine_random / 8 == 1:
                            field[x][y]['is_a_mine'] = True
                            mines_count += 1
                    else:
                        return field
            else:
                return field
    return field


def count_field_mines(rows, columns, field):
    for x in range(rows):
        for y in range(columns):
            field[x][y]['surrounding_mines'] += check_mine(x - 1, y + 1, field)
            field[x][y]['surrounding_mines'] += check_mine(x, y + 1, field)
            field[x][y]['surrounding_mines'] += check_mine(x + 1, y + 1, field)
            field[x][y]['surrounding_mines'] += check_mine(x - 1, y, field)
            field[x][y]['surrounding_mines'] += check_mine(x, y + 1, field)
            field[x][y]['surrounding_mines'] += check_mine(x - 1, y - 1, field)
            field[x][y]['surrounding_mines'] += check_mine(x, y - 1, field)
            field[x][y]['surrounding_mines'] += check_mine(x + 1, y - 1, field)
            # print(field[x][y]['surrounding_mines'])
    return field


def generate_field(rows, columns, mines):
    field = init_field(rows, columns)
    add_mines(rows, columns, field, mines)
    count_field_mines(rows, columns, field)
    return field

def int_input(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print(INVALID_NUM)


def input_opts(fake_game):
    options = {
        'rows': 20,
        'columns': 20,
        'mines': 20,
    }
    if fake_game:
        return options
    else:
        options['rows'] = int_input("Rows: ")
        options['columns'] = int_input("Columns: ")
        options['mines'] = int_input("Mines: ")
    return options


def choose_coords(rows, columns):
    print("\n--- You are now choosing coordinates ---")
    coords = {
            'x': -1,
            'y': -1,
    }
    while not ((coords['x'] >= 0) and (coords['x'] <= rows) and (coords['y'] >= 0) and (coords['y'] <= columns)):
        coords['x'] = int_input("X: ") - 1
        coords['y'] = int_input("Y: ") - 1
    return coords


def display_field(rows, columns, field, display):
    print('   ', end='')
    for x in range(columns):
        if x + 1 < 10:
            print(x + 1, end='  ')
        else:
            print(x + 1, end=' ')
    print()
    for y in range(rows):
        if y + 1 < 10:
            print(y + 1, end='  ')
        else:
            print(y + 1, end=' ')
        for x in range(rows):
            if field[x][y]['is_a_mine'] and display == 'surrounding_mines':
                print('x ', end=' ')
            else:
                print(field[x][y][display], end='  ')
        print() #  new line for each row


def reveal(field, coords):
    try:
        if field[coords['x']][coords['y']]['is_a_mine']:
            field[coords['x']][coords['y']]['display'] = 'X'
            return True, field
        field[coords['x']][coords['y']]['display'] = field[coords['x']][coords['y']]['surrounding_mines']
        if not field[coords['x']][coords['y'] + 1]['is_a_mine'] and field[coords['x']][coords['y'] + 1]['display'] != field[coords['x']][coords['y'] + 1]['surrounding_mines']:
            reveal(field, {'x': coords['x'], 'y': coords['y'] + 1})
        if not field[coords['x'] - 1][coords['y']]['is_a_mine'] and field[coords['x'] - 1][coords['y']]['display'] != field[coords['x'] - 1][coords['y']]['surrounding_mines']:
            reveal(field, {'x': coords['x'] - 1, 'y': coords['y']})
        if not field[coords['x'] + 1][coords['y']]['is_a_mine'] and field[coords['x'] + 1][coords['y']]['display'] != field[coords['x'] + 1][coords['y']]['surrounding_mines']:
            reveal(field, {'x': coords['x'] + 1, 'y': coords['y']})
        if not field[coords['x']][coords['y'] - 1]['is_a_mine'] and field[coords['x']][coords['y'] - 1]['display'] != field[coords['x']][coords['y'] - 1]['surrounding_mines']:
            reveal(field, {'x': coords['x'], 'y': coords['y'] - 1})
    except IndexError:
        pass
    # This is the recursion
    return False, field


def choose_tool():
    choice = 0
    print("--- Choose an option ---")
    for tool in TOOLS:
        print(tool)
    while not ((choice < len(TOOLS) + 1) and (choice >= 1)):
        choice = int_input("Choice: ")
    return choice


def flag_unflag(field, coords):
    '''
    if the spot has already been revealed:
        don't let the user flag it
    if

    '''
    pass


if __name__ == "__main__":
    options = input_opts(False)
    num_rows = options['rows']
    num_columns = options['columns']
    board_size = num_rows * num_columns
    field = generate_field(num_rows, num_columns, options['mines'])
    display_field(num_rows, num_columns, field, 'display')
    a_mine = [False]
    # Initialize the a_mine list

    # the actual game starts here
    while not a_mine[0]:
        tool = choose_tool()
        # choose your tool, reveal or flag
        coords = choose_coords(num_rows, num_columns)
        # choose your coordinates
        print("\n" * 50)
        # clear the screen
        if tool == 1:
            a_mine = reveal(field, coords)
            display_field(num_rows, num_columns, field, 'surrounding_mines')
            # Revealed field
            display_field(num_rows, num_columns, field, 'display')
            # Game field
        if tool == 2:
            flag_unflag(field, coords)
            display_field(num_rows, num_columns, field, 'surrounding_mines')
            # Revealed field
            display_field(num_rows, num_columns, field, 'display')
            # Game field
        if a_mine[0]:
            print("\n" * 50)
            # clear the screen
            display_field(num_rows, num_columns, field, 'surrounding_mines')
            # Revealed field
            print(LOSE)
            # the user lost, so tell them


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
