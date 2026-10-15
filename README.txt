CIS 524 — Interpreter

Project Description

This project implements an interpreter in Python using top-down recursive-descent parsing.

The interpreter reads a .tiny source file, checks whether the program follows the Tiny language grammar, and evaluates valid expressions.

How the Code Works

1. Tokenizer

The tokenize() function uses a regular expression (`TOKEN_PATTERN`) to separate the source code into tokens, including keywords, identifiers, numbers, and operators.

2. Recursive-Descent Parser

The `Parser` class contains functions corresponding to the grammar rules. The `get_token()` function retrieves the current token, and `check_token()` verifies the expected token and advances to the next one.

3. Variables and Data Types

The interpreter stores declared variables and their values. The `Value` class represents integer and real values.

4. Expression Evaluation

The `expression()`, `term()`, and `factor()` functions evaluate arithmetic expressions while respecting operator precedence. The interpreter also supports conditional expressions and type conversions.

5. Error Handling

If the interpreter encounters invalid syntax or an unsupported operation, it prints `Error`.

How to Run

Requirements: Python 3.10 or later.

Open a terminal in the project folder and run:

python parser_2564134.py sample.tiny

Output

30
314.16
0.25
Error

Project Files
- parser_2564134.py — Python interpreter
- sample.tiny — Sample Tiny language programs
- output.png — Screenshot of the program output
- README.txt — Project explanation and instructions
