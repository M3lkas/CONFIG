import unittest
import os
from PyQt5.QtWidgets import QApplication
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаем экземпляр QApplication для всех тестов"""
        cls.app = QApplication([])

    def setUp(self):
        self.test_dir = './vfs_test'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write("Test file content\n")
        self.emulator = ShellEmulator(start_dir=self.test_dir)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_ls(self):
        output = self.emulator.process_command('ls')
        self.assertIn('file1.txt', output)

    def test_touch(self):
        self.emulator.process_command('touch newfile.txt')
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'newfile.txt')))


if __name__ == '__main__':
    unittest.main()
