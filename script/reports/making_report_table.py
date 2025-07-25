from tabulate import tabulate
from typing import Any, Callable, Dict, List, Optional, Tuple
import exceptionts


def report_table(
        args: Any,
        reports: Dict[str, Callable[[Any], Tuple[List[List[Any]], List[str]]]],
        logs: Any
) -> Optional[str]:
    try:
        table_data, headers = reports[args.report](logs)
    except exceptionts.FileNotFoundInPath:
        raise
    except exceptionts.IncorrectFileFormat:
        raise
    except exceptionts.JSONDecodeError:
        raise
    except exceptionts.MissingKeyError:
        raise
    except exceptionts.InvalidKeyError:
        raise

    if table_data:
        return tabulate(table_data, headers=headers, tablefmt='grid')
    else:
        raise exceptionts.EmptyReport(
            message="Report dont have a data"
        )
