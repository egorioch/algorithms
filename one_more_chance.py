#  log() = [], pow() = {}
import math
import re

operations = {
    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
    "{": 4,
    "}": 4,
    "[": 4,
    "]": 4
}
'{} - log, [] - pow'


def is_number(n):
    try:
        float(n)
    except ValueError:
        return False
    return True


def first_sym_is_plus(expression):
    if expression[0] == '+':
        return expression[1:]
    else:
        return expression


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


def is_valid_parenthesis(expression):
    left_par = expression.count('(')
    right_par = expression.count(')')
    if left_par != right_par:
        raise ValueError("Несоответствие количества '(' и ')'")


def calculate_rpn(output_string):
    if len(output_string) == 1:
        return output_string.pop()
    elif len(output_string) == 2 and output_string[0] == "-" and is_number(output_string[1]):
        if float(output_string[1]) < 0:
            return f"{output_string[1]}"
        else:
            return f"{output_string[0]}{output_string[1]}"

    output_string = output_string
    while len(output_string) != 1:
        counter = 0
        while output_string[counter] not in operations:
            counter += 1
        if output_string[counter] in operations:
            operation = output_string.pop(counter)
            op1 = output_string.pop(counter - 1)
            op2 = output_string.pop(counter - 2)
            result = apply_operator(operation, float(op2), float(op1))
            output_string.insert(0, result)

    return result


def polnag(expression):
    input_string = expression
    stack = []
    output = []

    while input_string:
        value = list(reversed(input_string.split())).pop()
        if is_number(value):
            output.append(value)
        else:
            if not stack and value != ' ':
                stack.append(value)
            elif value in operations or value in "()":

                if value == "(":
                    stack.append(value)
                elif value == ")":
                    last_sym = stack.pop()
                    while last_sym != "(":
                        output.append(last_sym)
                        last_sym = stack.pop()
                elif value in "{[":
                    substring = input_string[input_string.index(value) + 2:input_string.index("}") - 1]
                    left_side = "".join(substring.split(" , ")[0])
                    right_side = "".join(substring.split(" , ")[1])

                    if any(char in operations.keys() for char in left_side):
                        left_side = calculate_rpn(polnag(left_side))
                    if any(char in operations.keys() for char in right_side):
                        right_side = calculate_rpn(polnag(right_side))

                    operation_res = math.log(float(left_side), float(right_side))
                    input_string = input_string.replace(input_string[input_string.index(value):input_string.index("}") + 1], str(operation_res))
                    # stack.append(value)
                    output.append(operation_res)
                elif value in "]}":
                    while stack and stack[-1] not in "{[":
                        output.append(stack.pop())
                    output.append(value)
                elif value in operations:
                    if stack[-1] == '(':
                        stack.append(value)
                    else:
                        while stack and operations[value] <= operations[stack[-1]]:
                            output.append(stack.pop())

                        stack.append(value)

    while stack:
        output.append(stack.pop())

    return output


try:
    expression = "8*{2+5*2, 4}"

    expression = re.sub(r'(?<![\+\-\*/])-(\d+)', r'+(0-\1)', first_sym_is_plus(expression))
    expression = re.sub(r'-(\d+)', r'(0-\1)', expression)
    expression = re.sub(r'--', r'+', expression)
    formatted_expression = re.sub(r'([+\-*/(),{}])', r' \1 ', expression)

    # Удаляем лишние пробелы
    formatted_expression = ' '.join(formatted_expression.split())
    print(formatted_expression)
    is_valid_parenthesis(formatted_expression)
    result = calculate_rpn(polnag(formatted_expression))
    print(result)

except ValueError as e:
    print(f"Ошибка: {e}")
