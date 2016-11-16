# coding=utf-8


def header():
    """
    Return the header for this work
    """
    header_string = '\nSimulador de Máquina de Turing ver 1.0'
    header_string += '\nDesenvolvido como trabalho prático para a disciplina de Teoria da Computação'
    header_string += '\nAutores: Bruno Tomé, Ronan Nunes'
    header_string += '\nIFMG, 2016.'

    return header_string


def get_block(_line):
    """
    Get the block of current line

    :param _line:
    :return:
    """
    block = _line.split()
    block = block[1]
    return block


# initialWord = raw_input('Forneça a palavra inicial: ')
#
# print initialWord

if __name__ == '__main__':
    print header()

    script = open('palindromo.MT', 'r')

    for line in script:
        if line.startswith(';'):
            continue
        if line.startswith('bloco'):
            print get_block(line)
