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
    lst = list(s)
    lst[i], lst[j] = lst[j], lst[i]
    return ''.join(lst)


def move_head_right():
    global tape

    tape = swap(tape, head_position - 1, head_position)
    tape = swap(tape, head_position + 1, head_position + 2)


def move_head_left():
    global tape

    tape = swap(tape, head_position, head_position + 1)
    tape = swap(tape, head_position - 2, head_position - 1)


def get_block(_line):
    """
    Get the block of current line

    :param _line:
    :return str:
    """
    _block = _line.split()
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


def get_initial_block_state(_line):
    """
    Get the initial state of block

    :param _line:
    :return int:
    """
    _initial_state = _line.split()
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


def get_current_state(_line):
    """
    Get the current state of non block line

    :param _line:
    :return int:
    """
    _state = _line.split()
    _state = _state[0]

    return _state


def get_next_state(_line):
    """
    Get the next state of non block line

    :param _line:
    :return int:
    """
    _state = _line.split()
    _state = _state[5]

    return _state


def get_next_block_state(_line):
    """
    Get the next state of non block line

    :param _line:
    :return int:
    """
    _state = _line.split()
    _state = _state[2]

    return _state


def get_current_symbol(_line):
    """
    Get the current symbol of non block line

    :param _line:
    :return str:
    """
    _symbol = _line.split()
    _symbol = _symbol[1]

    return _symbol


def get_next_symbol(_line):
    """
    Get the current symbol of non block line

    :param _line:
    :return str:
    """
    _symbol = _line.split()
    _symbol = _symbol[3]

    return _symbol


def get_direction(_line):
    """
    Get the direction

    :param _line:
    :return int:
    """
    _direction = _line.split()
    _direction = _direction[4]

    return _direction


def move_head_position(_line):
    global head_position

    _direction = get_direction(_line)

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


def update_tape(_line):
    """
    Update the content of the tape

    :param _line:
    """
    global tape

    _current_symbol = get_next_symbol(_line)

    if not is_asterisc(_current_symbol):
        tape = tape[:head_position] + get_next_symbol(_line) + tape[(head_position + 1):]


def output(_block, _state):
    """
    Create the final ouput for each line

    :param _block:
    :param _state:
    :return str:
    """
    global tape

    return fix_block_output(_block) + fix_state_output(_state) + tape


def read_blocks(_script):
    """
    Read all the lines and put into a list, foreach list and save the blocks

    :param _script:
    """

    global blocks

    lines = _script.readlines()
    lines = [x for x in lines if not x.startswith('    ;')]
    list_of_this_block = []
    block = 'main'

    for _line in lines:

        # Check if there is a block
        if _line.startswith('bloco'):
            block = get_block(_line)
            blocks[block] = ''
            continue
        elif _line.startswith(' '):
            list_of_this_block.append(_line)
        elif _line.startswith('fim'):
            blocks[block] = list_of_this_block
            list_of_this_block = []


def state_transition(_current_block, _line):
    global tape
    global head_position
    global blocks
    global stack

    if tape[head_position] == get_current_symbol(_line):
        update_tape(_line)
        if get_next_state(_line) == 'retorne':
            print(output(_current_block, get_current_state(_line)))
            return run(stack[len(stack) - 1], stack[len(stack) - 2])

    elif get_current_state(_line) == get_next_state(_line):
        for _index in blocks[_current_block]:
            _index_aux = _index.split()
            if _index_aux[0] == get_current_state(_index):
                # If position in the tape is equal to current symbol, write the new symbol to the tape

                if get_next_state(_index) == 'retorne':
                    print(output(_current_block, get_current_state(_index)))

                if tape[head_position] == get_current_symbol(_index):
                    update_tape(_index)
                    if get_next_state(_index) == 'retorne':
                        move_head_position(_index)
                        return run(stack[len(stack) - 1], stack[len(stack) - 2])

        move_head_position(_line)
        state_transition(_current_block, _line)


def run(_current_block, _next_state):
    """
    Run over the block lines

    :param _current_block:
    :param _next_state:
    """
    global tape
    global head_position

    print(output(_current_block, _next_state))

    for _line in blocks[_current_block]:
        if get_current_state(_line) == _next_state:
            # It's a line with format: <current state> <current symbol> -- <next symbol> <direction> <next state>
            if len(_line.split()) == 6:
                if tape[head_position] == get_current_symbol(_line):
                    _next_state = get_next_state(_line)
                    state_transition(_current_block, _line)
                else:
                    continue

            # It's a line with format: bloco <id> <initial_state>
            elif len(_line.split()) == 3:
                print(output(_current_block, get_current_state(_line)))
                _next_state = get_next_block_state(_line)
                if len(stack) != 0:
                    stack.pop()  # Remove block
                    stack.pop()  # Remove state
                stack.append(_next_state)
                stack.append(_current_block)

                _current_block = get_block(_line)

                for index in blocks[_current_block]:
                    if len(index.split()) == 6:
                        _next_state = get_next_state(index)
                        state_transition(_current_block, index)


def is_asterisc(_symbol):
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
