# coding=utf-8

tape = ''
head_position = 21  # The current position of head
blocks = {}  # All the blocks readed
block_stack = []  # Stack to back to previously block
state_stack = []  # Stack to back to previously state


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


def get_block_next_state(_line):
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


if __name__ == '__main__':
    print header()

    # initialWord = raw_input('Forneça a palavra inicial: ')
    initial_word = 'aba'

    script = open('palindromo.MT', 'r')

    set_initial_tape(initial_word)

    # Read all the file and put blocks into a list
    read_blocks(script)

    current_state = '01'
    current_block = 'main'
    print output(current_block, current_state)

    for line in blocks['main']:
        current_state = get_current_state(line)

        if current_state != get_current_state(line):
            print 'continue'
            continue
        elif len(line.split()) == 6:
            if tape[head_position] == get_current_symbol(line):
                update_tape(line)
                next_state = get_next_state(line)
                print output(current_block, next_state)
        elif len(line.split()) == 3:
            block_stack.append(current_block)
            current_block = get_block(line)
            for i in blocks[current_block]:
                print i
                exit(0)
