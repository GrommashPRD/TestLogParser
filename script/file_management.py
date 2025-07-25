import os
import json
import exceptionts

from script.logs_loader.filter import logsFilter

class FileManager:

    @staticmethod
    def find_file_for_a_path(file_path: str) -> None:
        if not os.path.exists(file_path):
            raise exceptionts.FileNotFoundInPath(
                message="Error: File not found: %s"
                        % file_path
            )
        if not os.path.isfile(file_path):
            raise exceptionts.IncorrectFileFormat(
                message="Error: Not a file: %s"
                        % file_path
            )

    @staticmethod
    def read_file(file_path, date_filter):
        log_filter = logsFilter.LogFilter

        try:
            FileManager.find_file_for_a_path(file_path)
        except exceptionts.FileNotFound:
            raise
        except exceptionts.IncorrectFileFormat:
            raise

        with open(file_path, 'r') as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    log = json.loads(line.strip())
                except json.JSONDecodeError as e:
                    raise exceptionts.JSONDecodeError(
                        message="Invalid JSON in file %s, line %s: %s"
                                % (file_path, line_number, e)
                    )
                if date_filter:
                    try:
                        log_date = log_filter.date_filter(log)
                    except KeyError:
                        raise exceptionts.MissingKeyError(
                            message="Missing '@timestamp' key in log: %s"
                                    % log
                        )
                    except ValueError:
                        raise exceptionts.InvalidKeyError(
                            message="Invalid timestamp format in log from file %s, line %s"
                                    % (file_path, line_number)
                        )
                    if log_date == date_filter:
                        yield log
                    continue
                yield log
