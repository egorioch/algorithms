import math


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def calculate_expression(expression):
    def apply_operator(op, x, y):
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        elif op == '*':
            return x * y
        elif op == '/':
            if y == 0:
                raise ValueError("Деление на ноль")
            return x / y
        elif op == 'log':
            if y <= 0 or x <= 0:
                raise ValueError("Логарифм аргументов должен быть положительным")
            return math.log(x, y)
        elif op == 'pow':
            return math.pow(x, y)
        else:
            raise ValueError(f"Недопустимый оператор: {op}")

    operators = []
    operands = []

    tokens = expression.split()

    for token in tokens:
        if is_number(token) or (token[0] == '-' and is_number(token[1:].isnumeric())):
            operands.append(float(token))
        elif token in ['+', '-', '*', '/', 'log', 'pow']:
            while (operators and operators[-1] in ['+', '-', '*', '/', 'log', 'pow'] and
                   (token in ['+', '-'] and operators[-1] in ['*', '/', 'log', 'pow'] or
                    token in ['*', '/'] and operators[-1] in ['log', 'pow'])):
                op = operators.pop()
                y = operands.pop()
                x = operands.pop()
                result = apply_operator(op, x, y)
                operands.append(result)
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators and operators[-1] != '(' or operators and operators[-2] == 'log':
                op = operators.pop()
                if op == '(':
                    raise ValueError("Несоответствие количества '(' и ')'")
                y = operands.pop()
                x = operands.pop()
                result = apply_operator(op, x, y)
                operands.append(result)
            if operators and operators[-1] == '(':
                operators.pop()
            else:
                raise ValueError("Несоответствие количества '(' и ')'")

    while operators:
        op = operators.pop()
        if op == '(':
            raise ValueError("Несоответствие количества '(' и ')'")
        y = operands.pop()
        x = operands.pop()
        result = apply_operator(op, x, y)
        operands.append(result)

    if len(operands) != 1:
        raise ValueError("Некорректное выражение")

    return operands[0]


try:
    expression = input("Введите арифметическое выражение: ")
    result = calculate_expression(expression)
    print(f"Результат: {result}")
except ValueError as e:
    print(f"Ошибка: {e}")
