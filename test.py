import re


def replace_double_minus(expression):
    def replace_match(match):
        # Если число минусов в совпадении четное, заменяем на "+", иначе на "-"
        return '+' if len(match.group(0)) % 2 == 0 else '-'

    # Заменяем все "--" на "+" или "-"
    expression = re.sub(r'--+', replace_match, expression)

    return expression


original_expression = "--5 -(-5) ++5 ---6"
formatted_expression = replace_double_minus(original_expression)
print(formatted_expression)
