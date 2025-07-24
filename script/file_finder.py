import os

from exceptionts import FileNotFoundInPath, IncorrectFileFormat

def find_file_for_a_path(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundInPath(message="Error: File not found: %s" % file_path)
    if not os.path.isfile(file_path):
        raise IncorrectFileFormat(message="Error: Not a file: %s" % file_path)
