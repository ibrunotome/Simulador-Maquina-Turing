# coding=utf-8
import re

tape = ''
head_position = 21  # The current position of head
blocks = {}  # All the blocks readed
stack = []


def header():
    """
    Return the header for this work
    """
    header_string = '\nSimulador de Máquina de Turing v1.0'
    header_string += '\nDesenvolvido como trabalho prático para a disciplina de Teoria da Computação.'
    header_string += '\nAutores: Bruno Tomé, Ronan Nunes.'
    header_string += '\nIFMG, 2016.\n'

    return header_string


def get_globals():
    global tape
    global head_position
    global stack

    print('\n\nGLOBALS\n')

    print('tape: ', tape)
    print('head_position: ', head_position)
    print('stack: ', stack)

    print('==================================================\n\n')


def swap(s, i, j):
    """
    Swap two chars

    :param s:
    :param i:
    :param j:
    :return:
    """

    lst = list(s)
    lst[i], lst[j] = lst[j], lst[i]

    return ''.join(lst)


def move_head_right():
    """
    Move to right the head indicator of the tape ( as default is () )
    """

    global tape
    global head_position

    tape = swap(tape, head_position - 1, head_position)
    tape = swap(tape, head_position + 1, head_position + 2)


def move_head_left():
    """
    Move to left the head indicator of the tape ( as default is () )
    """

    global tape
    global head_position

    tape = swap(tape, head_position, head_position + 1)
    tape = swap(tape, head_position - 2, head_position - 1)


def get_block(_row):
    """
    Get the block of current row

    :param _row:
    :return str:
    """

    _block = _row.split()
    _block = _block[1]

    return _block


def fix_block_output(_block):
    """
    Fix the block output in solicited format

    :param _block:
    :return str:
    """

    _block_fixed = ''
    for _i in range(0, (16 - len(_block))):
        _block_fixed += '.'

    return _block_fixed + _block + '.'


def get_initial_block_state(_row):
    """
    Get the initial state of block

    :param _row:
    :return int:
    """

    _initial_state = _row.split()
    _initial_state = _initial_state[2]

    return _initial_state


def fix_state_output(_state):
    """
    Fix the state output in the solicited format

    :param _state:
    :return str:
    """

    _state_fixed = ''
    for _i in range(0, (4 - len(_state))):
        _state_fixed += '0'

    return _state_fixed + _state + ':'


def get_current_state(_row):
    """
    Get the current state of non block row

    :param _row:
    :return int:
    """

    _state = _row.split()
    _state = _state[0]

    return _state


def get_next_state(_row):
    """
    Get the next state of non block row

    :param _row:
    :return int:
    """

    _state = _row.split()
    _state = _state[5]

    return _state


def get_next_block_state(_row):
    """
    Get the next state of block row

    :param _row:
    :return int:
    """

    _state = _row.split()
    _state = _state[2]

    return _state


def get_current_symbol(_row):
    """
    Get the current symbol of non block row

    :param _row:
    :return str:
    """

    _symbol = _row.split()
    _symbol = _symbol[1]

    return _symbol


def get_next_symbol(_row):
    """
    Get the current symbol of non block row

    :param _row:
    :return str:
    """

    _symbol = _row.split()
    _symbol = _symbol[3]

    return _symbol


def get_direction(_row):
    """
    Get the direction to go

    :param _row:
    :return int:
    """

    _direction = _row.split()
    _direction = _direction[4]

    return _direction


def move_head_position(_row):
    """
    Move the head to the right or left, or stay on the same symbol

    :param _row:
    """

    global head_position

    _direction = get_direction(_row)

    if _direction == 'd':
        move_head_right()
        head_position += 1
    elif _direction == 'e':
        move_head_left()
        head_position -= 1


def set_left_tape():
    """
    Set the initial left tape

    :return str:
    """

    _blank_space = ''
    for _i in range(0, 20):
        _blank_space += '_'

    return _blank_space


def set_right_tape(_initial_word):
    """
    Set the initial right tape

    :param _initial_word:
    :return str:
    """

    _blank_space = ''
    for _i in range(0, (20 - len(_initial_word))):
        _blank_space += '_'

    return _blank_space


def set_initial_head(_initial_word):
    """
    Put the head into the initial word

    :param _initial_word:
    :return:
    """

    return '(' + _initial_word[0] + ')' + _initial_word[1:]


def set_initial_tape(_initial_word):
    """
    Set the initial tape

    :param _initial_word:
    """

    global tape

    tape = set_left_tape() + set_initial_head(_initial_word) + set_right_tape(_initial_word)


def update_tape(_row):
    """
    Update the content of the tape

    :param _row:
    """

    global tape
    global head_position

    _current_symbol = get_next_symbol(_row)

    if not is_asterisc(_current_symbol):
        tape = tape[:head_position] + get_next_symbol(_row) + tape[(head_position + 1):]


def output(_block, _state):
    """
    Create the final ouput for each row

    :param _block:
    :param _state:
    :return str:
    """

    global tape

    return fix_block_output(_block) + fix_state_output(_state) + tape


def read_blocks(_script):
    """
    Read all the rows and put into a list, foreach list and save the blocks

    :param _script:
    """

    global blocks

    rows = _script.readlines()
    rows = [x for x in rows if not x.startswith('    ;') or not x.startswith(';')]
    list_of_this_block = []
    block = ''

    for _row in rows:

        # Check if there is a block
        if _row.startswith('bloco'):
            # It's a new block
            block = get_block(_row)
            continue
        elif _row.startswith(' '):
            # It's a new instrucion
            list_of_this_block.append(_row)
        elif _row.startswith('fim'):
            # It's time to put the instructions of this block into the block position
            blocks[block] = list_of_this_block
            list_of_this_block = []


def state_transition(_current_block, _row):
    """
    Make the transition between the states

    :param _current_block:
    :param _row:
    :return str:
    """

    global tape
    global head_position
    global blocks
    global stack

    # The content on the tape is equal to current symbol
    if tape[head_position] == get_current_symbol(_row):
        update_tape(_row)

        # If the next
        if get_next_state(_row) == 'retorne':
            return run(stack[len(stack) - 1], stack[len(stack) - 2])
    elif get_current_state(_row) == get_next_state(_row):
        # Foreach a sub-block
        for _row_of_block in blocks[_current_block]:

            # Walking on tape
            if get_next_state(_row_of_block) == 'retorne':
                print(output(_current_block, get_current_state(_row_of_block)))

            # If position in the tape is equal to current symbol, write the new symbol to the tape
            if tape[head_position] == get_current_symbol(_row_of_block):
                update_tape(_row_of_block)

                # If next state is 'retorne', call the last block of stack and go back to the last state of the stack
                if get_next_state(_row_of_block) == 'retorne':
                    move_head_position(_row_of_block)
                    return run(stack[len(stack) - 1], stack[len(stack) - 2])

        move_head_position(_row)
        state_transition(_current_block, _row)


def run(_current_block, _next_state):
    """
    Run over the block rows

    :param _current_block:
    :param _next_state:
    """

    global tape
    global head_position

    print(output(_current_block, _next_state))

    for _row in blocks[_current_block]:

        if get_current_state(_row) == _next_state:

            # It's a row with format: <current state> <current symbol> -- <next symbol> <direction> <next state>
            if len(_row.split()) == 6:
                if tape[head_position] == get_current_symbol(_row):
                    _next_state = get_next_state(_row)
                    state_transition(_current_block, _row)
                elif is_asterisc(get_current_symbol(_row)):
                    run(_current_block, get_next_state(_row))

            # It's a row with format: bloco <id> <initial_state>
            elif len(_row.split()) == 3:
                print(output(_current_block, get_current_state(_row)))
                _next_state = get_next_block_state(_row)
                if len(stack) != 0:
                    stack.pop()  # Remove block
                    stack.pop()  # Remove state
                stack.append(_next_state)
                stack.append(_current_block)

                _current_block = get_block(_row)

                for index in blocks[_current_block]:
                    if len(index.split()) == 6:
                        _next_state = get_next_state(index)
                        state_transition(_current_block, index)


def is_asterisc(_symbol):
    """
    Check if symbol is an asterisc

    :param _symbol:
    :return bool:
    """

    type_1 = re.compile('∗')
    type_2 = re.compile('\*')

    if type_1.match(_symbol) or type_2.match(_symbol):
        return True
    return False


if __name__ == '__main__':
    print(header())

    # initialWord = raw_input('Forneça a palavra inicial: ')
    initial_word = 'aba'

    script = open('palindromo.MT', 'r')

    set_initial_tape(initial_word)

    # Read all the file and put blocks into a list
    read_blocks(script)

    current_state = '01'
    next_state = '01'
    current_block = 'main'
    run(current_block, next_state)
