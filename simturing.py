# coding=utf-8

tape = ''
blocks = {}


def header():
    """
    Return the header for this work
    """
    header_string = '\nSimulador de Máquina de Turing ver 1.0'
    header_string += '\nDesenvolvido como trabalho prático para a disciplina de Teoria da Computação.'
    header_string += '\nAutores: Bruno Tomé, Ronan Nunes.'
    header_string += '\nIFMG, 2016.\n'

    return header_string


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
    for i in range(0, (16 - len(_block))):
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
    for i in range(0, (4 - len(_state))):
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


def set_left_tape():
    """
    Set the initial left tape

    :return str:
    """
    _blank_space = ''
    for i in range(0, 20):
        _blank_space += '_'

    return _blank_space


def set_right_tape(_initial_word):
    """
    Set the initial right tape

    :param _initial_word:
    :return str:
    """
    _blank_space = ''
    for i in range(0, (20 - len(_initial_word))):
        _blank_space += '_'

    return _blank_space


def set_initial_head(_initial_word):
    return '(' + _initial_word[0] + ')' + _initial_word[1:]


def set_initial_tape(_initial_word):
    global tape
    tape = set_left_tape() + set_initial_head(_initial_word) + set_right_tape(_initial_word)


if __name__ == '__main__':
    print header()

    # initialWord = raw_input('Forneça a palavra inicial: ')
    initial_word = 'aba'

    script = open('palindromo.MT', 'r')

    set_initial_tape(initial_word)

    lines = script.readlines()
    list_of_this_block = []
    block = 'main'

    for line in lines:
        # Jump comments
        if line.startswith(';'):
            continue

        # Check if there is a block
        if line.startswith('bloco'):
            block = get_block(line)
            blocks[block] = ''
            continue
        elif line.startswith(' '):
            list_of_this_block.append(line)
        elif line.startswith('fim'):
            blocks[block] = list_of_this_block
            list_of_this_block = []

    print blocks['moveFim']
