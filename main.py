import argparse
import logging
import os
import subprocess
import sys

from constants import DEFAULT_OUTPUT_DIRECTORY_NAME, VALID_IMAGE_EXTENSIONS, WINDOWS_CHECK_COMMAND, \
    DEFAULT_CHECK_COMMAND


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

def run_tesseract(filename,output_path,image_file_name):
    #Run tesseract
    filename_without_extension = os.path.splitext(filename)[0]
    text_file_path = os.path.join(output_path, filename_without_extension)
    subprocess.run(['tesseract',image_file_name, text_file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)

def main(input_path, output_path):
    # Check if tesseract is installed or not
    check_command = get_command()
    logging.debug("Running `{}` to check if tesseract is installed or not.".format(check_command))
    result = subprocess.run([check_command, 'tesseract'], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("tesseract-ocr missing, use install `tesseract` to resolve.")
        return
    logging.debug("Tesseract correctly installed!\n")

    # Check if a valid input directory is given or not
    if not check_path(input_path):
        logging.error("Nothing found at `{}`".format(input_path))
        return
    # Create output directory
    create_directory(output_path)
    
    #Check if input_path is directory or file      
    if os.path.isdir(input_path):

        # Check if input directory is empty or not
        total_file_count = len(os.listdir(input_path))
        if total_file_count == 0:
            logging.error("No files found at your input location")
            return

        # Iterate over all images in the input directory
        # and get text from each image
        other_files = 0
        successful_files = 0
        logging.info("Found total {} file(s)\n".format(total_file_count))
        for ctr, filename in enumerate(os.listdir(input_path)):
            logging.debug("Parsing {}".format(filename))
            extension = os.path.splitext(filename)[1]

            if extension.lower() not in VALID_IMAGE_EXTENSIONS:
                other_files += 1
                continue

            image_file_name = os.path.join(input_path, filename)
            run_tesseract(filename, output_path, image_file_name)
            successful_files += 1

        logging.info("Parsing Completed!\n")
        if successful_files == 0:
            logging.error("No valid image file found.")
            logging.error("Supported formats: [{}]".format(", ".join(VALID_IMAGE_EXTENSIONS)))
        else:
            logging.info("Successfully parsed images: {}".format(successful_files))
            logging.info("Files with unsupported file extensions: {}".format(other_files))
            
    else:
        filename = os.path.basename(input_path)
        run_tesseract(filename, output_path, filename)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', help="Input directory where input images are stored")
    parser.add_argument('--input_file', help="Input image filepath")
    parser.add_argument('--output_dir', nargs='?',
                        help="(Optional) Output directory for converted text (default: {input_path}/converted-text)")
    parser.add_argument('--debug', action='store_true',
                        help="Enable verbose DEBUG logging")
    args = parser.parse_args()
    if not args.input_dir and not args.input_file:
        parser.error('Required either --input_file or --input_dir')
    if args.input_dir:
        input_path = os.path.abspath(args.input_dir)
    else:
        input_path = os.path.abspath(args.input_file)
    if args.output_dir:
        output_path = os.path.abspath(args.output_dir)
    else:
        if os.path.isdir(input_path):
            output_path = os.path.join(input_path, DEFAULT_OUTPUT_DIRECTORY_NAME)
        else:
            dir_path = os.path.dirname(input_path)
            output_path = os.path.join(dir_path, DEFAULT_OUTPUT_DIRECTORY_NAME)


    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)
    main(input_path, output_path)
