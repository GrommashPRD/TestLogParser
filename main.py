import argparse
from datetime import datetime
from tabulate import tabulate
from script import loader, report_generators

reports = {
    'average': report_generators.generate_average_report,
    'User-Agents': report_generators.generate_user_agent_report
}


def main():
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

    try:
        args = parser.parse_args()
    except SystemExit:
        print("Error: Invalid command-line arguments. Please check usage.")
        return

    if args.date:
        try:
            date_filter = datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print(
                "Error: Invalid date format: $s Must be YYYY-MM-DD."
                % args.date
                )
            return
    else:
        date_filter = None

    logs = loader.load_logs(args.file, date_filter)
    if args.report in reports:
        table_data, headers = reports[args.report](logs)
        if table_data:
            print(tabulate(table_data, headers=headers, tablefmt='grid'))
        else:
            print("No data available for the report.")
    else:
        print("Error: Unknown report: %s" % args.report)


if __name__ == '__main__':
    main()
