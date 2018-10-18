import os
import unittest
from unittest import mock

import main as puc
from constants import WINDOWS_CHECK_COMMAND

resources_directory = "tests/resources"


class TestMain(unittest.TestCase):
    def test_create_directory(self):
        tmp_path = os.path.join(resources_directory, "temporary_directory_to_be_deleted")

        self.assertFalse(os.path.isdir(tmp_path))
        puc.create_directory(tmp_path)
        self.assertTrue(os.path.isdir(tmp_path))

        # clean up
        os.rmdir(tmp_path)

    def test_check_path_true(self):
        existing_file_path = os.path.join(resources_directory, "dummy_file")
        self.assertTrue(puc.check_path(existing_file_path))

    def test_check_path_false(self):
        unexisting_file_path = os.path.join(resources_directory, "not_existing_dummy_file")
        self.assertFalse(puc.check_path(unexisting_file_path))

    @mock.patch('main.sys.platform', return_value='win32')
    def test_get_command_windows(self, mocked_sys_platform):
        self.assertEqual(puc.get_command(), WINDOWS_CHECK_COMMAND)

    @mock.patch('main.subprocess.run')
    def test_missing_tesseract(self, mock_subprocess_run):
        "tesseract-ocr missing, use install `tesseract` to resolve"
        mock_subprocess_run.return_value.stdout = False

        empty_directory_location = os.path.join(resources_directory, "empty_directory")
        response = puc.main(empty_directory_location, resources_directory)
        self.assertIsNone(response)

    @mock.patch('main.subprocess.run')
    def test_empty_directory(self, mock_subprocess_run):
        "No files found at your input location"
        mock_subprocess_run.return_value.stdout = True

        empty_directory_location = os.path.join(resources_directory, "empty_directory")
        response = puc.main(empty_directory_location, resources_directory)
        self.assertIsNone(response)

    @mock.patch('main.subprocess.run')
    def test_invalid_directory(self, mock_subprocess_run):
        "No directory found"
        mock_subprocess_run.return_value.stdout = True

        empty_directory_location = os.path.join(resources_directory, "not_existing_empty_directory")
        response = puc.main(empty_directory_location, resources_directory)
        self.assertIsNone(response)

    @mock.patch('main.subprocess.run')
    def test_valid_directory(self, mock_subprocess_run):
        mock_subprocess_run.return_value.stdout = True

        directory = os.path.join(resources_directory, "test_directory")
        output_directory = os.path.join(directory, 'output')
        puc.main(directory, output_directory)
        self.assertTrue(os.path.isdir(output_directory))

        # cleanup
        os.rmdir(output_directory)


if __name__ == '__main__':
    unittest.main()
