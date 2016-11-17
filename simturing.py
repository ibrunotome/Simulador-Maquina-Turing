# coding=utf-8


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

    return _block_fixed + _block


def get_initial_block_state(_line):
    """
    Get the initial state of block

    :param _line:
    :return str:
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

    return _state_fixed + _state


def get_current_state(_line):
    """
    Get the current state of non block line

    :param _line:
    :return str:
    """
    _state = _line.split()
    _state = _state[0]

    return _state


def get_next_state(_line):
    """
    Get the next state of non block line

    :param _line:
    :return str:
    """
    _state = _line.split()
    _state = _state[5]

    return _state


# initialWord = raw_input('Forneça a palavra inicial: ')
#
# print initialWord

if __name__ == '__main__':
    print header()

    script = open('palindromo.MT', 'r')

    for line in script:
        # Jump comments
        if line.startswith(';'):
            continue

        # Check if there is a block
        if line.startswith('bloco'):
            block = get_block(line)
            block_output = fix_block_output(block) + '.'
            state = get_initial_block_state(line)
            state_output = fix_state_output(state)
            # print block_output + state_output

        if line.startswith(' '):
            current_state = get_current_state(line)
            next_state = get_next_state(line)
            print fix_state_output(current_state) + ' ' + fix_state_output(next_state)
            exit(0)
