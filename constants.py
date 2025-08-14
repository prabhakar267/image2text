DEFAULT_CHECK_COMMAND = "which"
WINDOWS_CHECK_COMMAND = "where"
TESSERACT_DATA_PATH_VAR = "TESSDATA_PREFIX"

VALID_IMAGE_EXTENSIONS = [
    # Common formats
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    # TIFF variants
    ".tif", ".tiff",
    # Modern formats
    ".webp", ".heic", ".heif",
    # Professional formats
    ".tga", ".psd", ".pcx",
    # Document formats
    ".pdf", ".jp2", ".j2k", ".jpf", ".jpx", ".jpm", ".mj2",
    # Raw and specialized formats
    ".pbm", ".pgm", ".ppm", ".pnm", ".pfm", ".pam",
    # Additional supported formats
    ".dib", ".rle", ".ico", ".cur"
]
