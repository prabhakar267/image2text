from __future__ import print_function
import unittest
from main import main
import builtins
import mock
import os
import tempfile


def side_effect(value):
    return value


class TestCore(unittest.TestCase):
    def test_setup(self):
        with mock.patch('builtins.print') as mock_print:
            output = main('sample', 'output')
            mock_print.assert_has_calls(
            [
                mock.call('tesseract-ocr missing, use sudo apt-get install '
                          'tesseract-ocr to resolve')
            ]
        )
        with mock.patch('builtins.print') as mock_print:
            output = main('not_a_dir', 'output')
            mock_print.assert_has_calls(
            [
                mock.call('No directory found at not_a_dir')
            ]
        )

    def test_output(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            main('sample', temp_dir)
            for file in os.listdir(temp_dir):
                with open('sample/converted-text/{}'.format(file)) as f1:
                    with open('temp_dir/{}'.format(file)) as f2:
                        self.assertEqual(f1.read(), f2.read())


if __name__ == '__main__':
    unittest.main()
