import sys
import json

def interpret(binary_file, memory_range):
    memory = [0] * 256  # допустим, у нас есть 256 ячеек памяти
    accumulator = 0
    pc = 0  # program counter
    results = {}

    with open(binary_file, 'rb') as f:
        bytecode = f.read()

    while pc < len(bytecode):
        command = bytecode[pc]
        if command == 0x01:  # LOAD
            pc += 1
            accumulator = bytecode[pc]
        elif command == 0x02:  # ADD
            pc += 1
            accumulator += bytecode[pc]
        elif command == 0x03:  # STORE
            pc += 1
            memory[bytecode[pc]] = accumulator
        elif command == 0x04:  # JUMP
            pc += 1
            pc = bytecode[pc]  # Переход на указанную позицию
            continue
        elif command == 0x05:  # HALT
            break
        else:
            raise ValueError(f"Неизвестная команда: {command}")
        pc += 1

    # Сохраняем результаты в JSON
    for i in range(memory_range[0], memory_range[1]):
        results[f"memory_{i}"] = memory[i]

    results["result"] = accumulator

    return results

if __name__ == "__main__":
    binary_file = sys.argv[1]
    memory_range = tuple(map(int, sys.argv[2].split(',')))
    results = interpret(binary_file, memory_range)

    with open('result.json', 'w') as f:
        json.dump(results, f, indent=2)
