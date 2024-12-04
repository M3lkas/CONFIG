import unittest
from dependency_analyzer import analyze_dependencies, generate_plantuml


class TestDependencyAnalyzer(unittest.TestCase):

    def test_analyze_dependencies(self):
        # Проверяем, что функция возвращает граф зависимостей
        graph = analyze_dependencies("pip")
        self.assertIn("pip", graph)
        self.assertIsInstance(graph["pip"], list)  # Проверяем, что зависимости — это список

    def test_generate_plantuml(self):
        # Проверяем, что функция корректно генерирует PlantUML-код
        graph = {"pip": ["setuptools", "wheel"], "setuptools": [], "wheel": []}
        uml_code = generate_plantuml(graph)
        self.assertIn('"pip" --> "setuptools"', uml_code)
        self.assertIn('"pip" --> "wheel"', uml_code)
        self.assertTrue(uml_code.startswith("@startuml"))
        self.assertTrue(uml_code.endswith("@enduml"))


if __name__ == "__main__":
    unittest.main()
