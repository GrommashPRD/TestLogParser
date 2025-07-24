import json
from typing import Generator, List, Optional, Any
from exceptionts import MissingKeyError, InvalidKeyError, JSONDecodeError, FileNotFoundInPath, \
    IncorrectFileFormat
from script import file_finder
from script.logs_loader.filter import logsFilter


def load_logs(
        files: List[str],
        date_filter: Optional[str]=None
) -> Generator[dict, None, None]:
    log_filter = logsFilter.LogFilter

    for file_path in files:
        try:
            file_finder.find_file_for_a_path(file_path)
        except FileNotFoundInPath:
            raise
        except IncorrectFileFormat:
            raise

        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    log = json.loads(line.strip())
                except json.JSONDecodeError as e:
                    raise JSONDecodeError(message="Invalid JSON in file %s, line %s: %s"
                        % (file_path, line_number, e))
                if date_filter:
                    try:
                        log_date = log_filter.date_filter(log)
                    except KeyError:
                        raise MissingKeyError(
                            message="Missing '@timestamp' key in log: %s"
                                    % log
                        )
                    except ValueError:
                        raise InvalidKeyError(
                            message="Invalid timestamp format in log from file %s, line %s"
                                    % (file_path, line_number)
                        )
                    if log_date == date_filter:
                        yield log
                else:
                    yield log
