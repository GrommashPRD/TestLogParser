from logger import logger
from datetime import datetime

import exceptionts
from script.logs_loader import loader
from script.parser import parser_constructor
from script.reports import making_report_table, report_generators

reports = {
    'average': report_generators.generate_average_report,
    'User-Agents': report_generators.generate_user_agent_report
}


def main():
    parser = parser_constructor.parser_preparing(reports)
    try:
        args = parser.parse_args()
    except SystemExit:
        logger.warning("Incorrect flag")
        return

    date_filter = datetime.strptime(args.date, '%Y-%m-%d').date() if args.date else None
    logs = loader.load_logs(args.file, date_filter)

    try:
        report_table = making_report_table.report_table(args, reports, logs)
    except exceptionts.FileNotFoundInPath as e:
        logger.warning("File mot found in path: %s" % e)
        return
    except exceptionts.IncorrectFileFormat as e:
        logger.warning("Incorrect File format: %s" % e)
        return
    except exceptionts.JSONDecodeError as e:
        logger.warning("Incorrect JSON data: %s" % e)
        return
    except exceptionts.MissingKeyError as e:
        logger.warning("Missing key: %s" %e)
        return
    except exceptionts.InvalidKeyError as e:
        logger.warning("Invalid key: %s" %e)
        return
    except exceptionts.ReportTypeNotExist as e:
        logger.warning("Report type is not exit %s" %e)
        return

    if report_table:
        print(report_table)

if __name__ == '__main__':
    main()
