; main
bloco main 1
    01 a -- A i 02
    01 b -- B i 04
    01 _ -- _ i 15
    15 sim pare
    02 moveFimA 03
    04 moveFimB 03
    03 moveInicio 01
fim

; A
bloco moveFimA 1
    01 * -- * d 01
    01 _ -- _ d 02
    02 A -- A d 02
    02 B -- B d 02
    02 _ -- A e retorne
fim

; B
bloco moveFimB 04
    04 * -- * d 04
    04 _ -- _ d 05
    05 A -- A d 05
    05 B -- B d 05
    05 _ -- B e retorne
fim

; I
bloco moveInicio 3
    03 * -- * e 03
    03 _ -- _ e 04
    04 * -- * e 04
    04 A -- a d retorne
    04 B -- b d retorne
fim

bloco sim 1
    01 * −− * d 02
    02 * −− S d 03
    03 * −− I d 04
    04 * −− M d retorne
fim ; sim