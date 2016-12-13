; Converte palavra maiúscula para minúscula a partir das pontas
bloco main 1
    01 A −− a i 10
    01 B −− b i 20
    01 a −− * i 70 ; Palavra já estava em minúsculo
    01 b -- * i 70 ; Palavra já estava em minúsculo
    10 moveFim 11
    20 moveFim 21

    ; leu a
    11 iniEsq 12
    12 A −− a i 30
    12 B −− * i 30
    12 _ −− * i 60

    ; leu b
    21 iniEsq 22
    22 A −− * i 30
    22 B −− a i 30
    22 _ −− * i 60

    30 moveIni 31
    31 iniDir 32
    32 _ −− * e 60
    32 * −− * i 01

    60 sim pare
    70 nao pare
fim ; main

; move para ultimo caractere da palavra
bloco moveFim 1
    01 _ −− * e retorne
    01 * −− * d 01
fim ; moveFim

; move para primeiro caractere da palavra
bloco moveIni 1
    01 _ −− * d retorne
    01 * −− * e 01
fim ; moveIni

; recua ate caractere minusculo ou _
bloco iniEsq 1
    01 _ −− * i retorne
    01 A −− * i retorne
    01 B −− * i retorne
    01 * −− * e 01
fim ; iniEsq

; avanca ate caractere minusculo ou _
bloco iniDir 1
    01 _ −− * i retorne
    01 A −− * i retorne
    01 B −− * i retorne
    01 * −− * d 01
fim ; iniDir

; Final da conversão
bloco sim 1
    01 moveFim 02
    02 * −− * d 03
    03 * −− S d 04
    04 * −− I d 05
    05 * −− M d retorne
fim ; sim

; Palavra já era minúscula
bloco nao 1
    01 moveFim 02
    02 * −− * d 03
    03 * −− N d 04
    04 * −− A d 05
    05 * −− O d retorne
fim ; nao