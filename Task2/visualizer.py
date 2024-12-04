import os
from dependency_analyzer import analyze_dependencies, generate_plantuml

def main():
    # Настройки проекта
    package_name = "requests"  # Укажите имя анализируемого пакета
    plantuml_path = "./plantuml-1.2024.8.jar"  # Относительный путь к PlantUML
    output_file = "output.puml"  # Путь для сохранения PlantUML-кода

    # Шаг 1: Анализ зависимостей
    print(f"Analyzing dependencies for package: {package_name}...")
    graph = analyze_dependencies(package_name)

    # Шаг 2: Генерация PlantUML
    print("Generating PlantUML code...")
    plantuml_code = generate_plantuml(graph)

    # Шаг 3: Сохранение PlantUML-кода
    with open(output_file, "w") as file:
        file.write(plantuml_code)
    print(f"PlantUML code saved to {output_file}")

    # Шаг 4: Генерация диаграммы через PlantUML
    print("Generating dependency diagram...")
    if os.path.exists(plantuml_path):
        os.system(f'java -jar "{plantuml_path}" "{output_file}"')
        print("Diagram generated successfully!")
    else:
        print(f"Error: PlantUML not found at {plantuml_path}")


if __name__ == "__main__":
    main()
