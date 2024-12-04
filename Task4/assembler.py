import sys
import json

# Пример команд и их кодов
command_map = {
    "LOAD": 0x01,
    "ADD": 0x02,
    "STORE": 0x03,
    "JUMP": 0x04,
    "HALT": 0x05
}


def assemble(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    binary_code = []
    log = {}

    for line in lines:
        # Удаляем лишние пробелы и пропускаем пустые строки
        line = line.strip()
        if not line:
            continue  # Пропускаем пустые строки

        parts = line.split()

        # Проверяем, что строка имеет правильный формат
        if len(parts) == 1:  # Это команда без аргумента
            command = parts[0]
            argument = None
        elif len(parts) == 2:  # Это команда с аргументом
            command = parts[0]
            try:
                argument = int(parts[1])
            except ValueError:
                print(f"Ошибка: аргумент '{parts[1]}' не является числом в строке '{line}'.")
                continue  # Пропускаем строки с некорректными аргументами
        else:
            print(f"Ошибка: строка '{line}' имеет некорректный формат.")
            continue  # Пропускаем строки с неправильным форматом

        if command in command_map:
            if argument is not None:  # Для команд с аргументом
                binary_command = [command_map[command], argument]
            else:  # Для команд без аргумента
                binary_command = [command_map[command]]
            binary_code.extend(binary_command)
            log[f"{command} {argument if argument is not None else ''}"] = binary_command
        else:
            print(f"Ошибка: неизвестная команда '{command}' в строке '{line}'.")
            continue  # Пропускаем строки с неизвестными командами

    # Запись бинарного кода в файл
    with open(output_file, 'wb') as f:
        f.write(bytes(binary_code))

    # Запись лога в JSON файл
    with open(log_file, 'w') as f:
        json.dump(log, f, indent=2)


if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    log_file = sys.argv[3]

    assemble(input_file, output_file, log_file)
