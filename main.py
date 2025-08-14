import argparse
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from constants import (DEFAULT_CHECK_COMMAND, TESSERACT_DATA_PATH_VAR,
                       VALID_IMAGE_EXTENSIONS, WINDOWS_CHECK_COMMAND)


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
    if sys.platform.startswith("win"):
        return WINDOWS_CHECK_COMMAND
    return DEFAULT_CHECK_COMMAND


def get_valid_image_files(input_path):
    """
    Efficiently get all valid image files from directory using pathlib
    :param input_path: Directory path to scan
    :return: List of valid image file paths
    """
    valid_files = []
    other_files = 0

    path = Path(input_path)

    # Use pathlib for more efficient file iteration
    for file_path in path.iterdir():
        if file_path.is_file():
            if file_path.suffix.lower() in VALID_IMAGE_EXTENSIONS:
                valid_files.append(file_path)
            else:
                other_files += 1

    return valid_files, other_files


def run_tesseract_optimized(image_path, output_path=None):
    """
    Optimized tesseract runner with better error handling and performance
    :param image_path: Path to image file
    :param output_path: Optional output directory
    :return: Tuple of (success, text_content, filename)
    """
    try:
        filename = image_path.name
        filename_without_extension = image_path.stem

        # If no output path is provided, return text directly
        if not output_path:
            # Use a single temp directory for the entire batch to reduce overhead
            temp_dir = tempfile.mkdtemp()
            temp_file = os.path.join(temp_dir, filename_without_extension)

            result = subprocess.run(
                ["tesseract", str(image_path), temp_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30  # Add timeout to prevent hanging
            )

            if result.returncode == 0:
                try:
                    with open(f"{temp_file}.txt", "r", encoding="utf8") as f:
                        text = f.read()
                    shutil.rmtree(temp_dir)
                    return True, text, filename
                except Exception as e:
                    logging.warning(f"Failed to read output for {filename}: {e}")
                    shutil.rmtree(temp_dir)
                    return False, None, filename
            else:
                logging.warning(
                    f"Tesseract failed for {filename}: {result.stderr.decode()}"
                )
                shutil.rmtree(temp_dir)
                return False, None, filename
        else:
            # Write directly to output directory
            text_file_path = os.path.join(output_path, filename_without_extension)
            result = subprocess.run(
                ["tesseract", str(image_path), text_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )

            if result.returncode == 0:
                return True, None, filename
            else:
                logging.warning(
                    f"Tesseract failed for {filename}: {result.stderr.decode()}"
                )
                return False, None, filename

    except subprocess.TimeoutExpired:
        logging.error(f"Tesseract timeout for {filename}")
        return False, None, filename
    except Exception as e:
        logging.error(f"Unexpected error processing {filename}: {e}")
        return False, None, filename


def run_tesseract(filename, output_path, image_file_name):
    """
    Legacy function for backward compatibility
    """
    image_path = Path(image_file_name)
    success, text, _ = run_tesseract_optimized(image_path, output_path)
    return text if success else ""


def check_pre_requisites_tesseract():
    """
    Check if the pre-requisites required for running the tesseract application are satisfied or not
    :param : NA
    :return: boolean
    """
    check_command = get_command()
    logging.debug("Running `{}` to check if tesseract is installed or not.".format(check_command))

    result = subprocess.run([check_command, "tesseract"], stdout=subprocess.PIPE)
    if not result.stdout:
        logging.error("tesseract-ocr missing, install `tesseract` to resolve. Refer to README for more instructions.")
        return False
    logging.debug("Tesseract correctly installed!\n")

    if sys.platform.startswith("win"):
        environment_variables = os.environ
        logging.debug("Checking if the Tesseract Data path is set correctly or not.\n")
        if TESSERACT_DATA_PATH_VAR in environment_variables:
            if environment_variables[TESSERACT_DATA_PATH_VAR]:
                path = environment_variables[TESSERACT_DATA_PATH_VAR]
                logging.debug(
                    "Checking if the path configured for Tesseract Data Environment variable `{}` \
                as `{}` is valid or not.".format(
                        TESSERACT_DATA_PATH_VAR, path
                    )
                )
                if os.path.isdir(path) and os.access(path, os.R_OK):
                    logging.debug("All set to go!")
                    return True
                else:
                    logging.error("Configured path for Tesseract data is not accessible!")
                    return False
            else:
                logging.error(
                    "Tesseract Data path Environment variable '{}' configured to an empty string!\
                ".format(
                        TESSERACT_DATA_PATH_VAR
                    )
                )
                return False
        else:
            logging.error(
                "Tesseract Data path Environment variable '{}' needs to be configured to point to\
            the tessdata!".format(
                    TESSERACT_DATA_PATH_VAR
                )
            )
            return False
    else:
        return True


def process_images_parallel(image_files, output_path, max_workers=None):
    """
    Process images in parallel using ThreadPoolExecutor
    :param image_files: List of image file paths
    :param output_path: Output directory path
    :param max_workers: Maximum number of worker threads
    :return: Tuple of (successful_files, failed_files, results)
    """
    if max_workers is None:
        # Use number of CPU cores, but cap at 8 to avoid overwhelming tesseract
        max_workers = min(8, os.cpu_count() or 4)

    successful_files = 0
    failed_files = 0
    results = []

    logging.info(f"Processing {len(image_files)} images using {max_workers} parallel workers...")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_image = {
            executor.submit(run_tesseract_optimized, image_path, output_path): image_path
            for image_path in image_files
        }

        # Process completed tasks
        for i, future in enumerate(as_completed(future_to_image), 1):
            image_path = future_to_image[future]

            try:
                success, text, filename = future.result()
                if success:
                    successful_files += 1
                    if text:  # Only store text if we're not writing to files
                        results.append((filename, text))
                else:
                    failed_files += 1

            except Exception as e:
                logging.error(f"Error processing {image_path.name}: {e}")
                failed_files += 1

            # Progress indicator
            if i % 10 == 0 or i == len(image_files):
                elapsed = time.time() - start_time
                rate = i / elapsed if elapsed > 0 else 0
                logging.info(
                    f"Progress: {i}/{len(image_files)} "
                    f"({i/len(image_files)*100:.1f}%) - {rate:.1f} files/sec"
                )

    total_time = time.time() - start_time
    logging.info(f"Parallel processing completed in {total_time:.2f} seconds")

    return successful_files, failed_files, results


def main(input_path, output_path, max_workers=None):
    # Check if tesseract is installed or not
    if not check_pre_requisites_tesseract():
        return

    # Check if a valid input directory is given or not
    if not check_path(input_path):
        logging.error("Nothing found at `{}`".format(input_path))
        return

    # Create output directory
    if output_path:
        create_directory(output_path)
        logging.debug("Creating Output Path {}".format(output_path))

    # Check if input_path is directory or file
    if os.path.isdir(input_path):
        logging.debug("The Input Path is a directory.")

        # Get valid image files efficiently
        image_files, other_files = get_valid_image_files(input_path)

        if len(image_files) == 0:
            logging.error("No valid image files found at your input location")
            logging.error(
                "Supported formats: [{}]".format(", ".join(VALID_IMAGE_EXTENSIONS))
            )
            return

        total_file_count = len(image_files) + other_files
        logging.info(
            "Found total {} file(s) ({} valid images, {} other files)\n".format(
                total_file_count, len(image_files), other_files
            )
        )

        # Process images in parallel
        successful_files, failed_files, results = process_images_parallel(image_files, output_path, max_workers)

        # Print results if not writing to files
        if not output_path:
            for filename, text in results:
                print(f"\n=== {filename} ===")
                print(text)

        logging.info("Parsing Completed!\n")
        logging.info("Successfully parsed images: {}".format(successful_files))
        if failed_files > 0:
            logging.warning("Failed to parse images: {}".format(failed_files))
        if other_files > 0:
            logging.info("Files with unsupported file extensions: {}".format(other_files))

    else:
        filename = os.path.basename(input_path)
        logging.debug("The Input Path is a file {}".format(filename))
        image_path = Path(input_path)
        success, text, _ = run_tesseract_optimized(image_path, output_path)
        if success and text:
            print(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "-i", "--input",
        help="Single image file path or images directory path",
        required=True
    )
    optional.add_argument("-o", "--output", help="(Optional) Output directory for converted text")
    optional.add_argument("-d", "--debug", action="store_true", help="Enable verbose DEBUG logging")
    optional.add_argument(
        "-w", "--workers",
        type=int,
        help="Number of parallel workers (default: auto-detect)",
        default=None
    )

    args = parser.parse_args()
    input_path = os.path.abspath(args.input)

    if args.output:
        output_path = os.path.abspath(args.output)
    else:
        output_path = None

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    logging.debug("Input Path is {}".format(input_path))

    # Check Python version
    if sys.version_info[0] < 3:
        logging.error(
            "You are using Python {0}.{1}. Please use Python>=3".format(
                sys.version_info[0], sys.version_info[1]
            )
        )
        exit()

    main(input_path, output_path, args.workers)
