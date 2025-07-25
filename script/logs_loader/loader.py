from typing import Generator, List, Optional, Any
import exceptionts
from script import file_management
fileManager = file_management.FileManager

def load_logs(
        files: List[str],
        date_filter: Optional[str] = None
) -> Generator[Any, None, None]:

    for file_path in files:
        try:
            fileManager.find_file_for_a_path(file_path)
        except exceptionts.FileNotFoundInPath:
            raise
        except exceptionts.IncorrectFileFormat:
            raise
        try:
            for log in fileManager.read_file(file_path, date_filter):
                yield log
        except exceptionts.JSONDecodeError:
            raise
        except exceptionts.MissingKeyError:
            raise
        except exceptionts.InvalidKeyError:
            raise
