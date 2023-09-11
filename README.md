[Raul Ikeda Gomes da Silva](http://lattes.cnpq.br/5935139039430914). Lógica de Computação. [Insper](https://github.com/Insper), 2023.

# compiler

![git status](http://3.129.230.99/svg/FelixLuciano/compiler/)

## Diagrama Sintático
```txt
EXPRESSION
         ┌──────┐
-> ─┼─ ->│ TERM ├─┼─ ->
    │    └──────┘ │
    │    ┌───┐    │
    ┼─ ->│ + ├────┼
    │    └───┘    │
    │    ┌───┐    │
    ┼─ ->│ - ├────┼
         └───┘

TERM
         ┌────────┐
-> ─┼─ ->│ FACTOR ├─┼─ ->
    │    └────────┘ │
    │    ┌───┐      │
    ┼─ ->│ * ├──────┼
    │    └───┘      │
    │    ┌───┐      │
    ┼─ ->│ / ├──────┼
         └───┘

Factor
         ┌────────┐
-> ─┼─ ->│ NUMBER ├──────────────────────┼─ ->
    │    └────────┘                      │
    │    ┌───┐      ┌────────┐           │
    ┼─ ->│ + ├─┼─ ->│ FACTOR ├───────────┼
    │    └───┘ │    └────────┘           │
    │    ┌───┐ │                         │
    ┼─ ->│ + ├─┤                         │
    │    └───┘                           │
    │   ┌───┐    ┌────────────┐    ┌───┐ │
    ┼ ->│ ( ├─ ->| EXPRESSION ├─ ->│ ) ├─┼
        └───┘    └────────────┘    └───┘
```

## EBMF
```txt
EXPRESSION = Term, {("+" | "-"), Term} ;
TERM       = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR     = ("+" | "-") FACTOR | "(" EXPRESSION ")" | number ;
NUMBER     = DIGIT, {DIGIT} ;
DIGIT      = 0 | 1 | 2 | 3 | 4 | 5 \ 6 | 7 | 8 | 9 ;
```
