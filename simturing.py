# coding=utf-8
import argparse
import sys

# Limit of recursions
sys.setrecursionlimit(20000)

out = ''
tape = ''
head_position = 21  # The current position of head
blocks = {}  # All the blocks readed
stack = []  # Stack to come back to the last block and state
verbose = False
resume = False
left_delimiter = '('
right_delimiter = ')'
steps = None
step = 0


def header():
    """
    Return the header for this work
    """

    header_string = '\nSimulador de Máquina de Turing v1.0'
    header_string += '\nDesenvolvido como trabalho prático para a disciplina de Teoria da Computação.'
    header_string += '\nAutor: Bruno Tomé.'
    header_string += '\nRepositório no GitHub: https://github.com/ibrunotome/Simulador-Maquina-Turing'
    header_string += '\nIFMG, 2016.\n'

    return header_string


def set_resume_true(*args):
    global resume

    resume = True


def set_resume_false(*args):
    global resume

    resume = False


def set_verbose_true(*args):
    global verbose

    verbose = True


def set_verbose_false(*args):
    global verbose

    verbose = False


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

    global head_position

    tape_list = list(s)

    try:
        tape_list[i], tape_list[j] = tape_list[j], tape_list[i]
    except IndexError:

        # Extend the tape size
        tape_list = ['_'] * 100 + tape_list
        tape_list += ['_'] * 100

        i += 6
        j += 4
        head_position += 5

        tape_list[i], tape_list[j] = tape_list[j], tape_list[i]

    return ''.join(tape_list)


def move_head_right():
    """
    Move to right the head indicator of the tape ( as default is () )
    """

    global tape
    global head_position

    tape = swap(tape, head_position - 1, head_position)
    tape = swap(tape, head_position + 1, head_position + 2)
    head_position += 1


def move_head_left():
    """
    Move to left the head indicator of the tape ( as default is () )
    """

    global tape
    global head_position

    tape = swap(tape, head_position, head_position + 1)
    tape = swap(tape, head_position - 2, head_position - 1)
    head_position -= 1


def get_block(_row):
    """
    Get the block of current row

    :param _row:
    :return str:
    """

    _block = _row.split()
    _block = _block[1]

    return _block


def fix_tape_output():
    global tape
    global head_position

    return tape[head_position - 20:head_position] + tape[head_position:head_position + 20]


def fix_block_output(_block):
    """
    Fix the block output in solicited format

    :param _block:
    :return str:
    """

    _block_fixed = ''
    for _i in xrange(0, (16 - len(_block))):
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
    for _i in xrange(0, (4 - len(_state))):
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
    elif _direction == 'e':
        move_head_left()


def set_left_tape_list():
    """
    Set the initial left tape

    :return str:
    """

    _blank_space = ''
    for _i in xrange(0, 20):
        _blank_space += '_'

    return _blank_space


def set_right_tape_list(_initial_word):
    """
    Set the initial right tape

    :param _initial_word:
    :return str:
    """

    _blank_space = ''
    for _i in xrange(0, (200 - len(_initial_word))):
        _blank_space += '_'

    return _blank_space


def set_initial_head(_initial_word):
    """
    Put the head into the initial word

    :param _initial_word:
    :return:
    """

    return left_delimiter + _initial_word[0] + right_delimiter + _initial_word[1:]


def set_initialtape_list(_initial_word):
    """
    Set the initial tape

    :param _initial_word:
    """

    global tape

    tape = set_left_tape_list() + set_initial_head(_initial_word) + set_right_tape_list(_initial_word)


def updatetape_list(_row):
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

    global out
    global tape
    global verbose
    global resume
    global step
    global steps

    out = fix_block_output(_block) + fix_state_output(_state) + fix_tape_output()

    if (verbose or steps) and not resume:
        print out

    if steps is not None:
        step += 1

    if step == steps:
        parameter = raw_input('New option (r, v, s): ')
        if parameter == 'r':
            verbose = False
            resume = True
        elif parameter == 'v':
            verbose = True
            resume = False
        elif parameter == 's':
            verbose = False
            resume = False
            steps = input('How much steps: ')
            step = 0
        else:
            step = 0


def read_blocks(_script):
    """
    Read all the rows and put into a list, foreach list and save the blocks

    :param _script:
    """

    global blocks

    rows = _script.readlines()
    list_of_this_block = []
    block = ''

    for _row in rows:

        if _row.startswith('    ;') or _row.startswith(';'):
            continue

        # Remove midle comments
        comment = _row.find(';')
        if comment != -1:
            _row = _row[:comment]

        # Check if there is a block
        if _row.startswith('bloco'):
            # It's a new block
            block = get_block(_row)
            continue
        elif _row.startswith(' '):
            # It's a new instruction
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
        updatetape_list(_row)

        # If the next state was 'retorne', come back one state in the stack
        if get_next_state(_row) == 'retorne':
            return run(stack[len(stack) - 1], stack[len(stack) - 2])

    elif get_current_state(_row) == get_next_state(_row):

        # Foreach a sub-block
        for _row_of_block in blocks[_current_block]:

            # Walking on tape
            if get_next_state(_row_of_block) == 'retorne':

                # It's the end of machine
                if (len(stack) > 0) and ((stack[len(stack) - 1] == 'sim') or (stack[len(stack) - 1] == 'nao')):
                    # Clear the stack
                    stack = []
                    return

                output(_current_block, get_current_state(_row_of_block))

            # If position in the tape is equal to current symbol, write the new symbol to the tape
            if tape[head_position] == get_current_symbol(_row_of_block):
                updatetape_list(_row_of_block)

                # If next state is 'retorne', call the block of stack and go back to the last state of the stack
                if get_next_state(_row_of_block) == 'retorne':
                    move_head_position(_row_of_block)
                    updatetape_list(_row_of_block)

                    # It's the end of machine
                    if len(stack) > 0:
                        return run(stack[len(stack) - 1], stack[len(stack) - 2])
                    else:
                        return

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

    output(_current_block, _next_state)

    for _row in blocks[_current_block]:

        # Head is on the left side of word in tape on the last block
        if get_block(_row) == 'sim' or get_block(_row) == 'nao':
            if tape[head_position] == '_':
                move_head_right()

        if get_current_state(_row) == _next_state:

            # It's a row with format: <current state> <current symbol> -- <next symbol> <direction> <next state>
            if len(_row.split()) == 6:

                if tape[head_position] == get_current_symbol(_row):
                    _next_state = get_next_state(_row)
                    state_transition(_current_block, _row)
                elif is_asterisc(get_current_symbol(_row)):
                    move_head_position(_row)
                    updatetape_list(_row)
                    return run(_current_block, get_next_state(_row))

            # It's a row with format: bloco <id> <initial_state>
            elif len(_row.split()) == 3:

                output(_current_block, get_current_state(_row))
                _next_state = get_next_block_state(_row)

                if len(stack) != 0:
                    stack.pop()  # Remove block
                    stack.pop()  # Remove state
                stack.append(_next_state)
                stack.append(_current_block)

                _current_block = get_block(_row)

                # It's a subblock of a block
                for index in blocks[_current_block]:

                    if len(index.split()) == 6:
                        _next_state = get_next_state(index)
                        state_transition(_current_block, index)
                    elif len(index.split()) == 3:

                        # It's the end
                        _next_state = get_next_block_state(index)
                        stack.append(_next_state)
                        stack.append(_current_block)

                        return run(get_block(index), '01')


def is_asterisc(_symbol):
    """
    Check if symbol is an asterisc

    :param _symbol:
    :return bool:
    """

    if _symbol == '∗' or _symbol == '*':
        return True
    return False


def get_parameters():
    """
    Change delimiter of tape
    """

    global left_delimiter
    global right_delimiter
    global steps

    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '-resume', dest='action', action='store_const', const=set_resume_true,
                        default=set_resume_false,
                        help='Print only final result.')
    parser.add_argument('-v', '-verbose', dest='action', action='store_const', const=set_verbose_true,
                        default=set_verbose_false,
                        help='Print step by step.')
    parser.add_argument('-s', '-step', help='Set the number of steps to verbose', type=int)
    parser.add_argument('-head', help='Change the delimiter')
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()
    args.action(args.args)

    if args.head is not None and len(args.head) == 2:
        left_delimiter = args.head[0]
        right_delimiter = args.head[1]

    if args.s is not None and args.s > 0:
        steps = args.s

    if not resume and not verbose and steps is None:
        print 'Run again using ONE of the following REQUIRED arguments:\n'
        print '-r/-resume: Print only final result'
        print '-v/-verbose: Print step by step'
        print '-s/-step: Print x steps'

        print '\nOptionally, you can change delimiter by using the argument -head "<delim>"\n'
        exit(0)


if __name__ == '__main__':

    # Work with the parameters
    get_parameters()

    print(header())

    initial_word = raw_input('Put the initial word: ')

    script = open(sys.argv[-1:][0], 'r')

    set_initialtape_list(initial_word)

    # Read all the file and put the blocks into a list
    read_blocks(script)

    current_state = '01'
    next_state = '01'
    current_block = 'main'
    run(current_block, next_state)

    if resume:
        print out
