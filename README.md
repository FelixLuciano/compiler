[Raul Ikeda Gomes da Silva](http://lattes.cnpq.br/5935139039430914). Lógica de Compuação. [Insper](https://github.com/Insper), 2023.

# compiler
![git status](http://3.129.230.99/svg/FelixLuciano/compiler/)

## Diagrama Sintático
```txt
Expression         |  Term
    /------\       |      /-----\     
-|->| Term |--|->  |  -|->| num |--|->
 |  \------/  |    |   |  \-----/  |  
 |            |    |   |           |  
 |    /---\   |    |   |   /---\   |  
 |----| + |---|    |   |---| * |---|  
 |    \---/   |    |   |   \---/   |  
 |            |    |   |           |  
 |    /---\   |    |   |   /---\   |  
 \----| - |---/    |   \---| / |---/  
      \---/        |       \---/      
```

## EBMF
```txt
EXPRESSION = NUMBER, {("+" | "-"), NUMBER} ;
NUMBER     = DIGIT, {DIGIT} ;
DIGIT      = 0 | 1 | 2 | 3 | 4 | 5 \ 6 | 7 | 8 | 9 ;
```
