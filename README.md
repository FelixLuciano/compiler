[Raul Ikeda Gomes da Silva](http://lattes.cnpq.br/5935139039430914). Lógica de Computação. [Insper](https://github.com/Insper), 2023.

# compiler

![git status](http://3.129.230.99/svg/FelixLuciano/compiler/)

## Diagrama Sintático
<details>
<summary>
  Click to reveal
</summary>

```txt
FILE
        ┌───────────┐     ╭─────────────╮
-> ┼─ ->│ STATEMENT ├┼─ ->│ END OF FILE ├─ ->
   │    └───────────┘│    ╰─────────────╯
   ┼ <- ─────────────┼

STATEMENT
                                                                                    ╭────╮
-> ─┼──────────────────────────────────────────────────────────────────────────┼─ ->│ \n ├─ ->
    │    ┌────────────┐                                                        │    ╰────╯
    ┼─ ->│ EXPRESSION ├────────────────────────────────────────────────────────┼
    │    └────────────┘                                                        │
    │      ╭────╮   ┌────────────┐   ┌───────┐                                 │
    ┼─┼─ ->│ IF ├ ->│ EXPRESSION ├ ->│ BLOCK ├┼────────────────────────────────┼
    │ │    ╰────╯   └────────────┘   └───────┘│    ╭──────╮     ┌───────┐      │
    │ │                                       ┼─ ->│ ELSE ├┼─ ->│ BLOCK ├──────┼
    │ │                                            ╰──────╯│    └───────┘      │
    │ ┼ <- ────────────────────────────────────────────────┼                   │
    │    ╭─────╮   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌───────┐│
    ┼─ ->│ FOR ├ ->│ EXPRESSION ├ ->│ EXPRESSION ├ ->│ EXPRESSION ├ ->│ BLOCK ├┼
         ╰─────╯   └────────────┘   └────────────┘   └────────────┘   └───────┘

EXPRESSION
         ┌────────────────────┐
-> ─┼─ ->│ BOOLEAN_EXPRESSION ├─ ->
    │    └────────────────────┘
    │    ┌────────────┐
    ┼─ ->│ IDENTIFIER ├─ -> ┼
    │    └────────────┘     │
    │    ╭───╮              │
    ┼────┤ = │<- ───────────┼
    │    ╰───╯ ╭────╮       │
    ┼──────────┤ += │<- ────┼
    │    ╭────╮╰────╯       │
    ┼────┤ -= │<- ──────────┼
    │    ╰────╯╭────╮       │
    ┼──────────┤ *= │<- ────┼
    │    ╭────╮╰────╯       │
    ┼────┤ /= │<- ──────────┼
         ╰────╯

BOOLEAN_EXPRESSION
         ┌──────────────┐
-> ─┼─ ->│ BOOLEAN_TERM ├─┼─ ->
    │    └──────────────┘ │
    │    ╭────╮           │
    ┼────┤ == │<- ────────┼
    │    ╰────╯╭────╮     │
    ┼──────────┤ != │<- ──┼
    │    ╭───╮ ╰────╯     │
    ┼────┤ > │<- ─────────┼
    │    ╰───╯ ╭────╮     │
    ┼──────────┤ >= │<- ──┼
    │    ╭───╮ ╰────╯     │
    ┼────┤ < │<- ─────────┼
    │    ╰───╯ ╭────╮     │
    ┼──────────┤ <= │<- ──┼
               ╰────╯

BOOLEAN_TERM
         ┌────────────────┐
-> ─┼─ ->│ BOOLEAN_FACTOR ├┼─ ->
    │    └────────────────┘│
    │    ╭────╮            │
    ┼────┤ || │<- ─────────┼
         ╰────╯

BOOLEAN_FACTOR
         ┌───────────────────────┐
-> ─┼─ ->│ ARITHMETIC_EXPRESSION ├┼─ ->
    │    └───────────────────────┘│
    │    ╭────╮                   │
    ┼────┤ && │<- ────────────────┼
         ╰────╯

ARITHMETIC_EXPRESSION
         ┌─────────────────┐
-> ─┼─ ->│ ARITHMETIC_TERM ├──────┼─ ->
    │    └─────────────────┘      │
    │    ╭───╮                    │
    ┼────┤ + │<- ─────────────────┼
    │    ╰───╯╭───╮               │
    ┼─────────┤ - │<- ────────────┼
              ╰───╯

ARITHMETIC_TERM
         ┌───────────────────┐
-> ─┼─ ->│ ARITHMETIC_FACTOR ├────┼─ ->
    │    └───────────────────┘    │
    │    ╭───╮         │
    ┼────┤ * │<- ──────┼
    │    ╰───╯╭───╮    │
    ┼─────────┤ / │<- ─┼
              ╰───╯

ARITHMETIC_FACTOR
         ╭───╮    ┌────────────────────┐    ╭───╮
-> ─┼─ ->│ ( ├─ ->│ BOOLEAN_EXPRESSION ├─ ->│ ) ├┼─ ->
    │    ╰───╯    └────────────────────┘    ╰───╯│
    │    ╭────────╮                              │
    ┼─ ->│ NUMBER ├──────────────┼───────────────┼
    │    ╰────────╯╭────────────╮│    ┌──────┐   │
    ┼─────────── ->│ IDENTIFIER ├┼─ ->│ CALL ├───┼
    │    ╭───╮     ╰────────────╯     └──────┘   │
    ┼─ ->│ + ├─────┼
    │    ╰───╯╭───╮│
    ┼────── ->│ - ├┼
    │    ╭───╮╰───╯│
    ┼─ ->│ ! ├─────┼
    │    ╰───╯     │
    ┼ <- ──────────┼

CALL
  ╭───╮     ┌────────────┐              ╭───╮
->│ ( ├┼─ ->│ EXPRESSION ├─────────┼─ ->│ ) ├─ ->
  ╰───╯│    └────────────┘╭───╮    │    ╰───╯
       ┼──────────────────┤ , │<- ─┼
                          ╰───╯

BLOCK
   ╭───╮    ╭────╮     ┌───────────┐     ╭───╮
-> │ { ├─ ->│ \n ├┼─ ->│ STATEMENT ├┼─ ->│ } ├─ ->
   ╰───╯    ╰────╯│    └───────────┘│    ╰───╯
                  ┼ <- ─────────────┼
```
</details>

## EBMF
<details>
<summary>
  Click to reveal
</summary>

```txt
FILE                  = { STATEMENT }, END OF FILE ;
STATEMENT             = ( λ | EXPRESSION | IF | FOR), "\n" ;
IF                    = "(IF", EXPRESSION, BLOCK) | "(IF", EXPRESSION, BLOCK, ELSE, BLOCK) | "(IF", EXPRESSION, BLOCK, ELSE, IF);
FOR                   = "FOR", EXPRESSION, EXPRESSION, EXPRESSION, BLOCK ;
EXPRESSION            = BOOLEAN_EXPRESSION | (IDENTIFIER , ("=" | "+=" | "-=" | "*=" | "/="), EXPRESSION)
BOOLEAN_EXPRESSION    = BOOLEAN_TERM, { ("==" | "!=" | ">" | "<" | ">=" | "<="), BOOLEAN_TERM } ;
BOOLEAN_TERM          = BOOLEAN_FACTOR, { "||", BOOLEAN_FACTOR } ;
BOOLEAN_FACTOR        = EXPRESSION, { "&&", EXPRESSION } ;
ARITHMETIC_EXPRESSION = TERM, { ("+" | "-"), TERM } ;
ARITHMETIC_TERM       = FACTOR, { ("*" | "/"), FACTOR } ;
ARITHMETIC_FACTOR     = ("(", BOOLEAN_EXPRESSION, ")") | NUMBER | IDENTIFIER | (IDENTIFIER, { CALL }) | ({ "+" | "-" | "!" }, FACTOR) ;
BLOCK                 = { STATEMENT } ;
CALL                  = "(", EXPRESSION, { ",", EXPRESSION }, ")" ;
NUMBER                = DIGIT, { DIGIT } ;
IDENTIFIER            = LETTER, { LETTER | DIGIT | "_" } ;
DIGIT                 = ( 0-9 ) ;
LETTER                = ( a-z | A-Z ) ;
```
</details>
