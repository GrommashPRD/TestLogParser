import argparse
from typing import Dict


def parser_preparing(reports: Dict[str, str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Log file processor')

    parser.add_argument(
        '--file',
        action='append',
        required=True,
        help='Path to log file (can be multiple)'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=reports.keys(),
        help='Report name'
    )
    parser.add_argument(
        '--date',
        help='Filter by date (YYYY-MM-DD)'
    )

    return parser
