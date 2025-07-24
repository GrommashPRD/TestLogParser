from tabulate import tabulate
from typing import Any, Callable, Dict, List, Optional, Tuple
from exceptionts import *


def report_table(
        args: Any,
        reports: Dict[str, Callable[[Any], Tuple[List[List[Any]], List[str]]]],
        logs: Any
) -> Optional[str]:
    try:
        table_data, headers = reports[args.report](logs)
    except FileNotFoundInPath:
        raise
    except IncorrectFileFormat:
        raise
    except JSONDecodeError:
        raise
    except MissingKeyError:
        raise
    except InvalidKeyError:
        raise

    if table_data:
        return tabulate(table_data, headers=headers, tablefmt='grid')
    else:
        return None
