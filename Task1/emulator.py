import os
import tarfile
import yaml
import json
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget


class ShellEmulator(QMainWindow):
    def __init__(self, config_path=None, start_dir=None):
        super().__init__()
        self.setWindowTitle("Shell Emulator")
        self.setGeometry(100, 100, 800, 600)

        # Если задан config_path, загружаем конфигурацию
        if config_path:
            self.config = self.load_config(config_path)
            self.user = self.config['user']
            self.host = self.config['host']
            self.log_file = self.config['log_file']
            self.startup_script = self.config['startup_script']
            self.current_dir = start_dir if start_dir else self.extract_vfs(self.config['vfs_archive'])
        else:
            # Для тестов используем start_dir
            self.user = "test_user"
            self.host = "test_host"
            self.log_file = "test_log.json"
            self.startup_script = None
            self.current_dir = start_dir if start_dir else os.getcwd()

        # Создаем интерфейс
        self.output_area = QTextEdit(self)
        self.output_area.setReadOnly(True)

        self.input_line = QLineEdit(self)
        self.input_line.returnPressed.connect(self.execute_command)

        # Размещение виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.output_area)
        layout.addWidget(self.input_line)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Выполняем стартовый скрипт
        if config_path and self.startup_script:
            self.run_startup_script()
        self.display_initial_message()

    @staticmethod
    def load_config(config_path):
        """Загрузка конфигурационного файла YAML"""
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def extract_vfs(archive_path, extract_to='./vfs'):
        """Распаковка виртуальной файловой системы"""
        if not os.path.exists(extract_to):
            os.makedirs(extract_to)
        with tarfile.open(archive_path, 'r') as tar:
            tar.extractall(path=extract_to)
        return extract_to

    def log_action(self, command):
        """Запись команд в лог-файл"""
        log_entry = {
            "datetime": datetime.now().isoformat(),
            "user": self.user,
            "command": command
        }
        with open(self.log_file, 'a') as log:
            log.write(json.dumps(log_entry) + '\n')

    def run_startup_script(self):
        """Выполнение команд из стартового скрипта"""
        if os.path.exists(self.startup_script):
            with open(self.startup_script, 'r') as file:
                for line in file:
                    command = line.strip()
                    self.process_command(command)

    def display_initial_message(self):
        """Вывод начального сообщения"""
        self.output_area.append("Welcome to the Shell Emulator!")
        self.output_area.append("Type 'ls', 'cd', 'touch', 'mv', 'tail', 'exit', etc. to interact.\n")
        self.write_prompt()

    def write_prompt(self):
        """Добавление приглашения к вводу"""
        self.output_area.append(f"{self.user}@{self.host}:{self.current_dir}$ ")

    def execute_command(self):
        """Обработка команды"""
        command = self.input_line.text().strip()
        self.log_action(command)
        self.output_area.append(f"$ {command}")
        self.input_line.clear()
        output = self.process_command(command)
        self.output_area.append(output)
        self.write_prompt()

    def process_command(self, command):
        """Обработка команд"""
        args = command.strip().split()
        if not args:
            return ""

        cmd = args[0]

        if cmd == "ls":
            try:
                return "\n".join(os.listdir(self.current_dir))
            except FileNotFoundError:
                return f"No such file or directory: {self.current_dir}"

        elif cmd == "cd":
            if len(args) < 2:
                return "cd: missing operand"
            target_dir = os.path.join(self.current_dir, args[1])
            if os.path.isdir(target_dir):
                self.current_dir = target_dir
                return ""
            else:
                return f"No such file or directory: {args[1]}"

        elif cmd == "touch":
            if len(args) < 2:
                return "touch: missing file operand"
            file_path = os.path.join(self.current_dir, args[1])
            with open(file_path, 'w') as f:
                pass
            return ""

        elif cmd == "mv":
            if len(args) < 3:
                return "mv: missing file operands"
            src = os.path.join(self.current_dir, args[1])
            dst = os.path.join(self.current_dir, args[2])
            try:
                os.rename(src, dst)
                return ""
            except FileNotFoundError:
                return f"mv: cannot move '{args[1]}' to '{args[2]}': No such file or directory"

        elif cmd == "tail":
            if len(args) < 2:
                return "tail: missing file operand"
            file_path = os.path.join(self.current_dir, args[1])
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                return "".join(lines[-10:])
            except FileNotFoundError:
                return f"tail: cannot open '{args[1]}' for reading: No such file"

        elif cmd == "exit":
            self.close()
            return "Exiting Shell Emulator. Goodbye!"

        else:
            return f"{cmd}: command not found"


if __name__ == "__main__":
    app = QApplication([])
    config_file = "config.yaml"
    emulator = ShellEmulator(config_file)
    emulator.show()
    app.exec()
