import math
import re

operators = {"(": 0, ")": 0, "+": 1, "-": 1, "*": 2, "/": 2, "pow": 3, "log": 3}


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def is_operand(token):
    return is_number(token)


def is_operator(token):
    return token in operators.keys()


def rpn(expression):
    stack = []
    out_string = []

    for token in expression.split():
        if is_number(token):
            out_string.append(token)
        elif token in "()":
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not out_string:
                    raise ValueError("Отсутствие выражения между скобками")
                if stack[-2] == 'log':
                    base = float(out_string.pop())
                    x = float(out_string.pop())
                    log_result = math.log(x, base)
                    out_string.append(log_result)
                    stack.pop()  # выбрасываем скобку
                    stack.pop()  # выбрасываем логарифм
                elif stack[-2] == 'pow':
                    base = float(out_string.pop())
                    x = float(out_string.pop())
                    log_result = math.pow(x, base)
                    out_string.append(log_result)
                    stack.pop()  # выбрасываем скобку
                    stack.pop()  # выбрасываем логарифм
                else:
                    while stack and stack[-1] != '(':
                        out_string.append(stack.pop())
                    stack.pop()
        elif is_operator(token):
            if len(stack) == 0:
                stack.append(token)
            else:
                if operators.get(token) <= operators.get(stack[-1]):
                    while stack and operators.get(stack[-1]) >= operators.get(token):
                        out_string.append(stack.pop())
                    stack.append(token)
                else:
                    stack.append(token)
    if stack:
        out_string += stack.pop()
    elif len(out_string) == 0:
        raise ValueError("Некорректное выражение")
    return out_string


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


def calculate_rpn(expression_array):
    if len(expression_array) == 1 or expression_array[0] == "-" and is_operand(expression_array[1]):
        return ''.join(expression_array)

    stack = []
    result = 0
    while expression_array:
        token = expression_array.pop()

        if is_operand(token):
            stack.append(token)
        else:
            second_operand = float(stack.pop())
            first_operand = float(stack.pop())
            result = apply_operator(token, first_operand, second_operand)
            expression_array.append(result)

    return result


def is_valid_parenthesis(expression):
    left_par = expression.count('(')
    right_par = expression.count(')')
    if left_par != right_par:
        raise ValueError("Несоответствие количества '(' и ')'")


try:
    expression = "-log(2, 4)"

    formatted_expression = re.sub(r'([+\-*/(),])', r' \1 ', expression)
    # Удаляем лишние пробелы
    formatted_expression = ' '.join(formatted_expression.split())
    print(formatted_expression)
    is_valid_parenthesis(formatted_expression)
    result = rpn(formatted_expression)
    rev = list(reversed(result))
    print(calculate_rpn(rev))

except ValueError as e:
    print(f"Ошибка: {e}")
