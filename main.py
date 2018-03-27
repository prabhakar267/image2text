# coding=utf-8

import sys
import os
from subprocess import call
import argparse

VALID_IMAGES = [".jpg", ".gif", ".png", ".tga", ".tif", ".bmp"]
FNULL = open(os.devnull, 'w')


class ArgumentMissingException(Exception):
    def __init__(self):
        print("usage: {} ".format(sys.argv[0]))
        sys.exit(1)


def create_directory(dir_path):
    if not os.path.exists(dir_path):

        os.makedirs(dir_path)


def check_path(dir_path):
    return bool(os.path.exists(dir_path))


def main(source, output_dir):
    current_directory = os.getcwd()
    destination = output_dir
    if not check_path(destination):
        destination = current_directory + output_dir
        create_directory(destination)
        if not check_path(destination):
            print(
                "I could not create or find '%s'" % destination
            )

    if call(['which', 'tesseract']):
        print("tesseract-ocr missing, use sudo apt-get install tesseract-ocr to resolve")
    elif check_path(source):

        count = 0
        other_files = 0
        print("Reading files from: %s" % source)
        print("Output destination is: %s" % destination)

        for f in os.listdir(source):
            ext = os.path.splitext(f)[1]

            if ext.lower() not in VALID_IMAGES:
                other_files += 1
                continue
            else:
                count += 1
                image_file_name = source + '/' + f
                filename = os.path.splitext(f)[0]
                filename = ''.join(e for e in filename if e.isalnum() or e == '-')
                text_file_path = "%s/%s" % (destination, filename)

                call(["tesseract", image_file_name, text_file_path], stdout=FNULL)

                print(str(count) + (" file" if count == 1 else " files") + " completed")

        if count + other_files == 0:
            print("No files found at your given location")
        else:
            print(str(count) + " / " + str(count + other_files) + " files converted")
    else:
        print("No directory found at " + format(source))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Ocr-convert-image-to-text arguments'
    )
    parser.add_argument(
        'input_dir', type=str, default='.', help='Path to directory of images'
    )
    parser.add_argument(
        '--output', "-o", type=str, default="/converted-text",
        help='Output path for text files'
    )

    args = parser.parse_args()
    src_path = os.path.abspath(args.input_dir)
    output_path = os.path.abspath(args.output)

    main(src_path, output_path)
