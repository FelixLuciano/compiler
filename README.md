[Raul Ikeda Gomes da Silva](http://lattes.cnpq.br/5935139039430914). Lógica de Computação. [Insper](https://github.com/Insper), 2023.

# compiler

![git status](http://3.129.230.99/svg/FelixLuciano/compiler/)

## Diagrama Sintático
```txt
STATEMENT
                                                                       ╭────╮    
-> ─┼─────────────────────────────────────────────────────────────┼─ ->│ \n ├─ ->
    │    ╭────────────╮     ╭───╮    ┌────────────┐               │    ╰────╯ 
    ┼─ ->│ IDENTIFIER ├┼─ ->│ = ├─ ->│ EXPRESSION ├───────────────┼
         ╰────────────╯│    ╰───╯    └────────────╯               │
                       │    ╭───╮    ┌────────────┐     ╭───╮     │
                       ┼─ ->│ ( ├┼ ->│ EXPRESSION ├┼─ ->│ ) ├─ -> ┼
                            ╰───╯│   └────────────┘│    ╰───╯
                                 │        ╭───╮    │
                                 ┼────────┤ , │<- ─┼
                                          ╰───╯

EXPRESSION
         ┌──────┐
-> ─┼─ ->│ TERM ├─┼─ ->
    │    └──────┘ │
    │    ╭───╮    │
    ┼─ ->│ + ├────┼
    │    ╰───╯    │
    │    ╭───╮    │
    ┼─ ->│ - ├────┼
         ╰───╯

TERM
         ┌────────┐
-> ─┼─ ->│ FACTOR ├─┼─ ->
    │    └────────┘ │
    │    ╭───╮      │
    ┼─ ->│ * ├──────┼
    │    ╰───╯      │
    │    ╭───╮      │
    ┼─ ->│ / ├──────┼
         ╰───╯

FACTOR
         ╭────────╮
-> ─┼─ ->│ NUMBER ├───────────────────────┼─ ->
    │    ╰────────╯                       │
    │    ╭────────────╮                   │
    ┼─ ->│ IDENTIFIER ├───────────────────┼
    │    ╰────────────╯                   │
    │    ╭───╮      ┌────────┐            │
    ┼─ ->│ + ├─┼─ ->│ FACTOR ├────────────┼
    │    ╰───╯ │    └────────┘            │
    │    ╭───╮ │                          │
    ┼─ ->│ + ├─┤                          │
    │    ╰───╯                            │
    │    ╭───╮    ┌────────────┐    ╭───╮ │
    ┼─ ->│ ( ├─ ->│ EXPRESSION ├─ ->│ ) ├─┼
         ╰───╯    └────────────┘    ╰───╯
```

## EBMF
```txt
BLOCK = { STATEMENT };
STATEMENT = ( λ | ASSIGNMENT | CALL), "\n" ;
ASSIGNMENT = IDENTIFIER, "=", EXPRESSION ;
CALL       = IDENTIFIER, "(", EXPRESSION, { ",", EXPRESSION }, ")" ;
EXPRESSION = Term, { ("+" | "-"), Term } ;
TERM       = FACTOR, { ( "*" | "/" ), FACTOR } ;
FACTOR     = ({"+" | "-"}, FACTOR) | "(" EXPRESSION ")" | IDENTIFIER ;
NUMBER     = DIGIT, { DIGIT } ;
IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
DIGIT      = ( 0-9 ) ;
LETTER     = ( a-z | A-Z ) ;
```
