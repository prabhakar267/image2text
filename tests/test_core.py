from __future__ import print_function
import unittest
from unittest.mock import MagicMock
from main import main
import builtins
import mock


def side_effect(value):
    return value

class TestCore(unittest.TestCase):
    def test_setup(self):
        from mock import call
        with mock.patch('builtins.print') as mock_print:
            output = main('sample','output')
            mock_print.assert_has_calls(
            [
                call("tesseract-ocr missing, use sudo apt-get install tesseract-ocr to resolve")
            ]
        )


if __name__ == '__main__':
    unittest.main()
