import re
import sys

class TinyError(Exception):
    pass

class Value:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

TOKEN_PATTERN = re.compile(r'\s+|\d+\.\d+|\d+|[A-Za-z_][A-Za-z_0-9]*|<=|>=|==|<>|[;:()=+*/<>-]')

def tokenize(source):
    tokens = []
    pos = 0
    while pos < len(source):
        match = TOKEN_PATTERN.match(source, pos)
        if match is None:
            raise TinyError()
        token = match.group()
        if not token.isspace():
            tokens.append(token)
        pos = match.end()
    tokens.append('<EOF>')
    return tokens

def cast(value, kind):
    if kind == 'int':
        return Value('int', int(value.value))
    return Value('real', float(value.value))

def arithmetic(left, right, operator):
    a = left.value
    b = right.value
    if operator == '+':
        result = a + b
    elif operator == '-':
        result = a - b
    elif operator == '*':
        result = a * b
    else:
        if b == 0:
            raise TinyError()
        result = a / b
    kind = 'real' if operator == '/' or left.kind == 'real' or right.kind == 'real' else 'int'
    return Value(kind, float(result) if kind == 'real' else int(result))

class Parser:
    def __init__(self, source):
        self.tokens = tokenize(source)
        self.pos = 0
        self.variables = {}

    def get_token(self):
        return self.tokens[self.pos]

    def check_token(self, expected):
        if self.get_token() != expected:
            raise TinyError()
        self.pos += 1

    def identifier(self):
        token = self.get_token()
        if not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', token):
            raise TinyError()
        if token in ('let', 'in', 'end', 'int', 'real', 'if', 'then', 'else'):
            raise TinyError()
        self.pos += 1
        return token

    def type_name(self):
        token = self.get_token()
        if token not in ('int', 'real'):
            raise TinyError()
        self.pos += 1
        return token

    def lookup(self, name):
        if name not in self.variables:
            raise TinyError()
        return self.variables[name]

    def program(self):
        if self.get_token() == "<EOF>":
            raise TinyError()

        while self.get_token() != "<EOF>":
            result = self.let_in_end()
            print(result)

    def let_in_end(self):
        self.check_token('let')
        self.variables = {}
        self.declaration()
        while self.get_token() != 'in':
            self.declaration()
        self.check_token('in')
        kind = self.type_name()
        self.check_token('(')
        result = self.expression()
        self.check_token(')')
        self.check_token('end')
        self.check_token(';')
        return cast(result, kind).value

    def declaration(self):
        name = self.identifier()
        self.check_token(':')
        kind = self.type_name()
        self.check_token('=')
        value = self.expression()
        self.check_token(';')
        if name in self.variables:
            raise TinyError()
        self.variables[name] = cast(value, kind)

    def expression(self):
        if self.get_token() == 'if':
            self.check_token('if')
            condition = self.condition()
            self.check_token('then')
            yes = self.expression()
            self.check_token('else')
            no = self.expression()
            return yes if condition else no
        result = self.term()
        while self.get_token() in ('+', '-'):
            operator = self.get_token()
            self.pos += 1
            right = self.term()
            result = arithmetic(result, right, operator)
        return result

    def term(self):
        result = self.factor()
        while self.get_token() in ('*', '/'):
            operator = self.get_token()
            self.pos += 1
            right = self.factor()
            result = arithmetic(result, right, operator)
        return result

    def factor(self):
        token = self.get_token()
        if token == '(':
            self.check_token('(')
            result = self.expression()
            self.check_token(')')
            return result
        if token in ('int', 'real'):
            kind = self.type_name()
            self.check_token('(')
            name = self.identifier()
            self.check_token(')')
            return cast(self.lookup(name), kind)
        if re.fullmatch(r'\d+(?:\.\d+)?', token):
            self.pos += 1
            if '.' in token:
                return Value('real', float(token))
            return Value('int', int(token))
        return self.lookup(self.identifier())

    def operand(self):
        token = self.get_token()
        if re.fullmatch(r'\d+', token):
            self.pos += 1
            return Value('int', int(token))
        return self.lookup(self.identifier())

    def condition(self):
        left = self.operand().value
        operator = self.get_token()
        if operator not in ('<', '<=', '>', '>=', '==', '<>'):
            raise TinyError()
        self.pos += 1
        right = self.operand().value
        if operator == '<':
            return left < right
        if operator == '<=':
            return left <= right
        if operator == '>':
            return left > right
        if operator == '>=':
            return left >= right
        if operator == '==':
            return left == right
        return left != right


def main():
    try:
        if len(sys.argv) != 2:
            raise TinyError()
        with open(sys.argv[1], encoding='utf-8') as file:
            source = file.read()
        parser = Parser(source)
        parser.program()
    except (TinyError, OSError, ValueError,
        ZeroDivisionError, OverflowError, IndexError):
        print("Error")


if __name__ == '__main__':
    main()
