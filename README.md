[Raul Ikeda Gomes da Silva](http://lattes.cnpq.br/5935139039430914). Lógica de Computação. [Insper](https://github.com/Insper), 2023.

# compiler

![git status](http://3.129.230.99/svg/FelixLuciano/compiler/)

## Diagrama Sintático
<details>
<summary>
  Click to reveal
</summary>

### `FILE`
```txt
    ┌────────────────┐╭─────────────╮
-> ─┤ STATEMENT_LIST ├┤ END_OF_FILE ├─ ->
    └────────────────┘╰─────────────╯
```

### `STATEMENT_LIST`
```txt
-> ┼────────────── -> ┼───────────────────────── -> ┼─ ->
   │┌───────────┐     │╭────╮┌────────────────┐     │
   ┼┤ STATEMENT ├─ -> ┼┤ \n ├┤ STATEMENT_LIST ├─ -> │
    └───────────┘      ╰────╯└────────────────┘
```

### `STATEMENT`
```txt
-> ─┼───────────────────────────────────────────────────────── -> ┼─ ->
    │╭─────╮          ┌───────────────┐                           │
    ┼┤ VAR ├──────────┤ VAR_STATEMENT ├─────────────────────── -> │
    │╰─────╯╭────╮    └───────────────┘┌──────────────┐           │
    ┼───────┤ IF ├─────────────────────┤ IF_STATEMENT ├─────── -> │
    │╭─────╮╰────╯    ┌───────────────┐└──────────────┘           │
    ┼┤ FOR ├──────────┤ FOR_STATEMENT ├─────────────────────── -> │
    │╰─────╯╭──────╮  └───────────────┘┌────────────────────┐     │
    ┼───────┤ FUNC ├───────────────────┤ FUNCTION_STATEMENT ├─ -> │
    │       ╰──────╯  ┌────────────┐   └────────────────────┘     │
    ┼─────────────────┤ EXPRESSION ├─────────────────────────  -> │
                      └────────────┘
```

### `VARIABLE_STATEMENT`
```txt
    ┌────────────┐┌────────────┐
-> ─┤ IDENTIFIER ├┤ IDENTIFIER ├┼──────────────────────────── -> ┼─ ->
    └────────────┘└────────────┘│╭───╮┌────────────────────┐     │
                                ┼┤ = ├┤ BOOLEAN_EXPRESSION ├─ -> │
                                 ╰───╯└────────────────────┘
```

### `IF_STATEMENT`
```txt
    ┌────────────┐┌───────┐
-> ─┤ EXPRESSION ├┤ BLOCK ├┼───────────────────────────────────────── -> ┼─ ->
    └────────────┘└───────┘│╭──────╮ ┌───────┐                           │
                           ┼┤ ELSE ├┼┤ BLOCK ├─────────────────────── -> │
                            ╰──────╯│└───────┘╭────╮┌──────────────┐     │
                                    ┼─────────┤ IF ├┤ IF_STATEMENT ├─ -> │
                                              ╰────╯└──────────────┘
```

### `FOR_STATEMENT`
```txt
    ┌────────────┐╭───╮┌────────────┐╭───╮┌────────────┐┌───────┐
-> ─┤ EXPRESSION ├┤ ; ├┤ EXPRESSION ├┤ ; ├┤ EXPRESSION ├┤ BLOCK ├─ ->
    └────────────┘╰───╯└────────────┘╰───╯└────────────┘└───────┘
```

### `FUNCTION_STATEMENT`
```txt
    ┌────────────┐╭───╮┌────────────┐╭───╮┌────────────┐┌───────┐
-> ─┤ IDENTIFIER ├┤ ( ├┤ EXPRESSION ├┤ ) ├┤ IDENTIFIER ├┤ BLOCK ├─ ->
    └────────────┘╰───╯└────────────┘╰───╯└────────────┘└───────┘
```

### `BLOCK`
```txt
    ╭───╮╭────╮┌────────────────┐╭───╮
-> ─┤ { ├┤ \n ├┤ STATEMENT_LIST ├┤ } ├─ ->
    ╰───╯╰────╯└────────────────┘╰───╯
```

### `EXPRESSION`
```txt
                                      ┌──────────────────────┐
-> ─┼──────────────────────────── -> ┼┤ EXPRESSION_CONDITION ├─ ->
    │┌────────────┐                  │└──────────────────────┘
    ┼┤ IDENTIFIER ├┼───────────── -> │
     └────────────┘│╭───╮            │
                   ┼┤ = ├──────── -> │
                   │╰───╯ ╭────╮     │
                   ┼──────┤ += ├─ -> │
                   │╭────╮╰────╯     │
                   ┼┤ -= ├─────── -> │
                   │╰────╯╭────╮     │
                   ┼──────┤ *= ├─ -> │
                   │╭────╮╰────╯     │
                   ┼┤ /= ├─────── -> │
                    ╰────╯
```

### `EXPRESSION_CONDITION`
```txt
   ┌─────────────────┐
-> │ EXPRESSION_TERM ├┼───────────────────────────────────── -> ┼─ ->
   └─────────────────┘│╭────╮            ┌─────────────────┐    │
                      ┼┤ == ├─────── -> ┼┤ EXPRESSION_TERM ├ -> │
                      │╰────╯╭────╮     │└─────────────────┘
                      ┼──────┤ != ├─ -> │
                      │╭───╮ ╰────╯     │
                      ┼┤ > ├──────── -> │
                      │╰───╯ ╭────╮     │
                      ┼──────┤ >= ├─ -> │
                      │╭───╮ ╰────╯     │
                      ┼┤ < ├──────── -> │
                      │╰───╯ ╭────╮     │
                      ┼──────┤ <= ├─ -> │
                             ╰────╯
```

### `EXPRESSION_TERM`
```txt
   ┌───────────────────┐
-> │ EXPRESSION_FACTOR ├┼────────────────────────── -> ┼─ ->
   └───────────────────┘│╭────╮┌─────────────────┐     │
                        ┼┤ || ├┤ EXPRESSION_TERM ├─ -> │
                         ╰────╯└─────────────────┘
```

### `EXPRESSION_FACTOR`
```txt
   ┌────────────────────┐
-> │ EXPRESSION_SUMMAND ├┼────────────────────────────────┼─ ->
   └────────────────────┘│╭────╮┌───────────────────┐     │
                         ┼┤ && ├┤ EXPRESSION_FACTOR ├─ -> │
                          ╰────╯└───────────────────┘
```

### `EXPRESSION_SUMMAND`
```txt
   ┌────────────────────┐
-> │ EXPRESSION_PRODUCT ├┼───────────────────────────────────────────┼─ ->
   └────────────────────┘│╭───╮           ┌────────────────────┐     │
                         ┼┤ + ├────── -> ┼┤ EXPRESSION_SUMMAND ├─ -> │
                         │╰───╯╭───╮     │└────────────────────┘
                         ┼─────┤ - ├─ -> │
                               ╰───╯
```
### `EXPRESSION_PRODUCT`
```txt
   ┌────────┐
-> │ FACTOR ├┼───────────────────────────────────────────┼─ ->
   └────────┘│╭───╮           ┌────────────────────┐     │
             ┼┤ * ├────── -> ┼┤ EXPRESSION_PRODUCT ├─ -> │
             │╰───╯╭───╮     │└────────────────────┘
             ┼─────┤ / ├─ -> │
                   ╰───╯
```

### `FACTOR`
```txt
     ╭───╮┌──────────────────────┐╭───╮
-> ─┼┤ ( ├┤ EXPRESSION_CONDITION ├┤ ) ├─ -> ┼─────────────────────── -> ┼─ ->
    │╰───╯└──────────────────────┘╰───╯     │╭───╮                      │
    │╭────────╮                             ┼┤ ! ├────────────────── -> │
    ┼┤ NUMBER ├───────────────────────── -> │╰───╯                      │
    │╰────────╯╭────────────╮               │╭───╮       ┌────────┐     │
    ┼──────────┤ IDENTIFIER ├┼────────── -> ┼┤ % ├── -> ┼┤ FACTOR ├─ -> │
    │╭───╮     ╰────────────╯│┌──────┐      │╰───╯      │└────────┘ 
    ┼┤ + ├────── -> │        ┼┤ CALL ├── -> │╭────╮     │
    │╰───╯╭───╮     │         └──────┘      ┼┤ ** ├─ -> │
    ┼─────┤ - ├─ -> │                        ╰────╯     │
    │╭───╮╰───╯     │                                   │
    ┼┤ ! ├────── -> ┼───────────────────────────────────┼
     ╰───╯
```

### `CALL`
```txt
    ╭───╮                          ╭───╮
-> ─┤ ( ├┼──────────────────── -> ┼┤ ) ├─ ->
    ╰───╯│┌─────────────────┐     │╰───╯
         ┼┤ EXPRESSION_LIST ├─ -> │
          └─────────────────┘
          
```

### `EXPRESSION_LIST`
```txt
    ┌────────────┐                                   
-> ─┤ EXPRESSION ├─ -> ┼───────────────────────── -> ┼─ ->
    └────────────┘     │╭───╮┌─────────────────┐     │
                       ┼┤ , ├┤ EXPRESSION_LIST ├─ -> │
                        ╰───╯└─────────────────┘
```
</details>

## EBMF
<details>
<summary>
  Click to reveal
</summary>

```txt

DIGIT                   = ( 0-9 ) ;
LETTER                  = ( a-z | A-Z ) ;
ENDL                    = ( \n ) ;
NUMBER                  = DIGIT, { DIGIT } ;
IDENTIFIER              = LETTER, { LETTER | DIGIT | "_" } ;
FILE                    = STATEMENT_LIST, END_OF_FILE ;
STATEMENT_LIST          = [ STATEMENT ], [ ENDL, STATEMENT_LIST ] ;
STATEMENT               = "var", VARIABLE_STATEMENT
                        | "if", IV_STATEMENT
                        | "for", FOR_STATEMENT
                        | "func", FUNCTION_STATEMENT
                        | EXPRESSION ;
VARIABLE_STATEMENT      = IDENTIFIER, IDENTIFIER, [ "=",BOOLEAN_EXPRESSION  ] ;
IF_STATEMENT            = EXPRESSION, BLOCK
                        | EXPRESSION, BLOCK, "else", BLOCK
                        | EXPRESSION, BLOCK, "else", "if", IF_STATEMENT ;
FOR_STATEMENT           = EXPRESSION, ";", EXPRESSION, ";", EXPRESSION, BLOCK ;
FUNCTION_STATEMENT      = IDENTIFIER, "(", EXPRESSION, ")", IDENTIFIER, BLOCK ;
BLOCK                   = "{", ENDL, STATEMENT_LIST, "}";
EXPRESSION              = [ IDENTIFIER, ( "=" | "+=" | "-=" | "*=" | "/=" ) ], EXPRESSION_CONDITION ;
EXPRESSION_CONDITION    = EXPRESSION_TERM, [ ( "==" | "!=" | ">" | ">=" | "<" | "<=" ), EXPRESSION_TERM ] ;
EXPRESSION_TERM         = EXPRESSION_FACTOR, [ "||", EXPRESSION_TERM ] ;
EXPRESSION_FACTOR       = EXPRESSION_SUMMAND, [ "&&", EXPRESSION_FACTOR ] ;
EXPRESSION_SUMMAND      = EXPRESSION_PRODUCT, [ ( "+" | "-" ), EXPRESSION_SUMMAND ] ;
EXPRESSION_PRODUCT      = FACTOR, [ ( "*" | "/" ), EXPRESSION_PRODUCT ] ;
FACTOR                  = { ("+", "-", "!") }, ( "(", EXPRESSION_CONDITION, ")" | NUMBER |IDENTIFIER, [ CALL ] ), [ "!" | ( "%", "**" ), FACTOR ] ;
CALL                    = "(", [ EXPRESSION_LIST ], ")";
EXPRESSION_LIST         = EXPRESSION, [ ",", EXPRESSION_LIST ] ;
```
</details>
