import argparse
import logging
import os
import subprocess
import sys

from constants import DEFAULT_OUTPUT_DIRECTORY_NAME, VALID_IMAGE_EXTENSIONS, WINDOWS_CHECK_COMMAND, \
    DEFAULT_CHECK_COMMAND, TESSERACT_DATA_PATH_VAR


def create_directory(path):
    """
    Create directory at given path if directory does not exist
    :param path:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)


def check_path(path):
    """
    Check if file path exists or not
    :param path:
    :return: boolean
    """
    return bool(os.path.exists(path))


def get_command():
    """
    Check OS and return command to identify if tesseract is installed or not
    :return:
    """
    if sys.platform.startswith('win'):
        return WINDOWS_CHECK_COMMAND
    return DEFAULT_CHECK_COMMAND


def check_pre_requisites_tesseract():
    """
    Check if the pre-requisites required for running the tesseract application are satisfied or not
    :param : NA
    :return: boolean
    """
    check_command = get_command()
    logging.debug("Running `{}` to check if tesseract is installed or not.".format(check_command))
    result = subprocess.run([check_command, 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("tesseract-ocr missing, use install `tesseract` to resolve.")
        return False
    logging.debug("Tesseract correctly installed!\n")

    if sys.platform.startswith('win'):
        environment_variables = os.environ
        logging.debug("Checking if the Tesseract Data path is set correctly or not.\n")
        if TESSERACT_DATA_PATH_VAR in environment_variables:
            if environment_variables[TESSERACT_DATA_PATH_VAR]:
                path = environment_variables[TESSERACT_DATA_PATH_VAR]
                logging.debug("Checking if the path configured for Tesseract Data Environment variable `{}` \
                as `{}` is valid or not.".format(TESSERACT_DATA_PATH_VAR, path))
                if os.path.isdir(path) and os.access(path, os.R_OK):
                    logging.debug("All set to go!")
                    return True
                else:
                    logging.error("Configured path for Tesseract data is not accessible!")
                    return False
            else:
                logging.error("Tesseract Data path Environment variable '{}' configured to an empty string!\
                ".format(TESSERACT_DATA_PATH_VAR))
                return False
        else:
            logging.error("Tesseract Data path Environment variable '{}' needs to be configured to point to\
            the tessdata!".format(TESSERACT_DATA_PATH_VAR))
            return False
    else:
        return True


def main(input_path, output_path, file_name):
    # Check if tesseract is installed or not
    if not check_pre_requisites_tesseract():
        return

    file_specified = file_name is not None

    # Check if a valid input directory is given or not
    if not check_path(input_path):
        logging.error("No {} found at `{}`".format("file" if file_specified else "directory", input_path))
        return

    # Check if input directory is empty or not
    total_file_count = 1 if file_specified else len(os.listdir(input_path))
    if total_file_count == 0:
        logging.error("No files found at your input location")
        return

    # Create output directory
    create_directory(output_path)

    # Iterate over all images in the input directory in case file_name argument is not specified
    # and get text from each image
    other_files = 0
    successful_files = 0
    logging.info("Found total {} file(s)\n".format(total_file_count))
    for ctr, filename in enumerate([file_name]) if file_specified else enumerate(os.listdir(input_path)):
        logging.debug("Parsing {}".format(filename))
        extension = os.path.splitext(filename)[1]

        if extension.lower() not in VALID_IMAGE_EXTENSIONS:
            other_files += 1
            continue

        image_file_name = os.path.join(input_path, filename)
        filename_without_extension = os.path.splitext(filename)[0]
        text_file_path = os.path.join(output_path, filename_without_extension)
        subprocess.run(['tesseract', image_file_name, text_file_path],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        logging.debug("Successfully parsed {}".format(filename))
        successful_files += 1

    logging.info("Parsing Completed!\n")
    if successful_files == 0:
        logging.error("No valid image file found.")
        logging.error("Supported formats: [{}]".format(", ".join(VALID_IMAGE_EXTENSIONS)))
    else:
        logging.info("Successfully parsed images: {}".format(successful_files))
        logging.info("Files with unsupported file extensions: {}".format(other_files))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', help="Input directory where input images are stored", required=True)
    parser.add_argument('--file_name', nargs='?',
                        help="(Optional) Image file name")
    parser.add_argument('--output_dir', nargs='?',
                        help="(Optional) Output directory for converted text (default: {input_path}/converted-text)")
    parser.add_argument('--debug', action='store_true',
                        help="Enable verbose DEBUG logging")
    args = parser.parse_args()

    input_path = os.path.abspath(args.input_dir)
    if args.output_dir:
        output_path = os.path.abspath(args.output_dir)
    else:
        output_path = os.path.join(input_path, DEFAULT_OUTPUT_DIRECTORY_NAME)
    if args.file_name:
        file_name = args.file_name
    else:
        file_name = None
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    main(input_path, output_path, file_name)
