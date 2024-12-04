import xml.etree.ElementTree as ET


def convert_to_postfix(expression):
    """Простой алгоритм для преобразования выражения в постфиксную форму.
    Здесь мы добавляем скобки для обеспечения правильного порядка операций.
    """
    expression = expression.replace(' ', '')

    # Преобразуем выражение с добавлением скобок
    # Например: (1 + 2) * 3 -> ((1 + 2) * 3)
    if '(' in expression and ')' in expression:
        expression = f"({expression})"

    return expression


def convert_to_custom_language(xml_root):
    """Конвертируем структуру XML в пользовательский язык конфигурации."""
    result = []

    for element in xml_root:
        if element.tag == "comment":
            if element.get("type") == "single-line":
                result.append(f"; {element.text.strip()}")
            elif element.get("type") == "multi-line":
                result.append("{#")
                result.append(f"{element.text.strip()}")
                result.append("#}")

        elif element.tag == "dictionary":
            result.append("$[")
            for item in element:
                key = item.get("name")
                value = item.text.strip()
                result.append(f"  {key}: {value},")
            result.append("]")

        elif element.tag == "constant":
            name = element.get("name")
            value = element.text.strip()
            result.append(f"set {name} = {value}")

        elif element.tag == "expression":
            expression = element.text.strip()
            postfix_expr = convert_to_postfix(expression)
            result.append(f"?{postfix_expr}")

        elif element.tag == "string":
            value = element.text.strip()
            result.append(f"@\"{value}\"")

    # Чтобы результат был на одной строке для многострочных комментариев
    formatted_result = "\n".join(result).replace("\n{#", "{#").replace("\n#}", "#}")
    return formatted_result


def save_to_file(output_data, output_file):
    """Сохраняем результат конвертации в файл."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_data)
