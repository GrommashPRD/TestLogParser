from datetime import datetime
from typing import Dict, Any

class LogFilter:

    @staticmethod
    def date_filter(log: Dict[str, Any]) -> datetime.date:
        try:
            log_date_str = log[
                '@timestamp'
            ].replace('Z', '+00:00')
        except KeyError:
            raise KeyError("Missing '@timestamp' key in log: %s" % log)

        try:
            log_date = datetime.fromisoformat(
                log_date_str
            ).date()
        except ValueError:
            raise ValueError("Invalid timestamp format in log from file %s" %log)

        return log_date