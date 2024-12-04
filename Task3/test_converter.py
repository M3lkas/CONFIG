import unittest
import xml.etree.ElementTree as ET
from converter import convert_to_custom_language


class TestConverter(unittest.TestCase):

    def test_convert_to_custom_language(self):
        input_xml = '''<root>
            <comment type="single-line">Это однострочный комментарий</comment>
            <comment type="multi-line">Это многострочный
            комментарий</comment>
            <dictionary>
                <item name="ключ1">значение1</item>
                <item name="ключ2">значение2</item>
            </dictionary>
            <constant name="CONST">123</constant>
            <expression>(1+2)*3</expression>
            <string>Пример строки</string>
        </root>'''

        expected_output = '''; Это однострочный комментарий
{#
Это многострочный комментарий
#}
$[
  ключ1: значение1,
  ключ2: значение2,
]
set CONST = 123
?((1+2)*3)
@"Пример строки"'''

        root = ET.fromstring(input_xml)
        result = convert_to_custom_language(root)

        self.assertEqual(result.strip(), expected_output.strip())


if __name__ == '__main__':
    unittest.main()
