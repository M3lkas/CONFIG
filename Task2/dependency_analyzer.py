import subprocess


def analyze_dependencies(package_name):
    """
    Анализирует зависимости Python-пакета, включая транзитивные.
    """
    def get_dependencies(pkg):
        result = subprocess.run(
            ["pip", "show", pkg],
            stdout=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            return []
        dependencies = []
        for line in result.stdout.split("\n"):
            if line.startswith("Requires:"):
                raw_deps = line.split(":", 1)[1].strip()
                dependencies = raw_deps.split(", ") if raw_deps else []
        return dependencies

    visited = set()
    stack = [package_name]
    graph = {}

    while stack:
        current_pkg = stack.pop()
        if current_pkg in visited:
            continue
        visited.add(current_pkg)
        deps = get_dependencies(current_pkg)
        graph[current_pkg] = deps
        stack.extend(dep for dep in deps if dep not in visited)

    return graph


def generate_plantuml(graph):
    """
    Генерирует PlantUML-код из графа зависимостей.
    """
    uml_lines = ["@startuml"]
    for pkg, deps in graph.items():
        for dep in deps:
            uml_lines.append(f'"{pkg}" --> "{dep}"')
    uml_lines.append("@enduml")
    return "\n".join(uml_lines)
