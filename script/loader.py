import os
import json
from datetime import datetime


def load_logs(files, date_filter=None):
    for file_path in files:
        try:
            if not os.path.exists(file_path):
                print("Error: File not found: %s" % file_path)
                continue
            if not os.path.isfile(file_path):
                print("Error: Not a file: %s" % file_path)
                continue
            with (open(file_path, 'r') as file):
                for line_number, line in enumerate(file, start=1):
                    try:
                        log = json.loads(line.strip())
                        if date_filter:
                            try:
                                log_date_str = log[
                                    '@timestamp'
                                ].replace('Z', '+00:00')
                                log_date = datetime.fromisoformat(
                                    log_date_str
                                ).date()
                                if log_date == date_filter:
                                    yield log
                            except KeyError:
                                print(
                                    "Error: Missing '@timestamp' key \
                                    in log from file %s, line %s"
                                    % (file_path, line_number)
                                )
                            except ValueError as e:
                                print(
                                    "Error: Invalid timestamp format \
                                    in log from file %s, line %s: %s"
                                    % (file_path, line_number, e)
                                )
                        else:
                            yield log
                    except json.JSONDecodeError as e:
                        print(
                            "Error: Invalid JSON in file %s, line %s: %s"
                            % (file_path, line_number, e)
                            )
        except PermissionError:
            print(
                "Error: Permission denied when trying to open file: %s"
                % file_path
            )
