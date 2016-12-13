# Simulador Máquina de Turing

Criação de um simulador de Máquina de Turing. Trabalho realizado no 8º período de Ciência da Computação no Instituto Federal de Minas Gerais (IFMG) - Campus Formiga para a disciplina de Teoria da Computação.

## Como usar
    python simturing.py <opções> <fonte.MT>

As opções podem ser:

    -resume (ou -r), executa o programa até o fim e depois imprime o conteúdo final na fita.
    -verbose (ou -v), mostra a execução passo a passo do programa até o fim.
    -step <n> (ou -s <n>), mostra n linhas de execução passo a passo na tela, depois abre prompt e aguarda nova opção (r, v, s). Caso não seja fornecida nova opção (entrada em branco), o padrão é repetir a última opção.
    -head "<delimitador>", altera o delimitador do cabeçote