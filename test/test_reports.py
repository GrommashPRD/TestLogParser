import sys

import pytest
from datetime import datetime

from unittest.mock import patch, Mock

import exceptionts
from main import main
from script.logs_loader import loader
from script.reports import report_generators
from script.reports.making_report_table import report_table

@pytest.fixture
def sample_log_file(tmp_path):
    data = [
        '{"@timestamp": "2023-10-01T12:00:00Z", "url": "/api/v1", "response_time": 0.5, "http_user_agent": "Mozilla/5.0"}',
        '{"@timestamp": "2023-10-01T12:01:00Z", "url": "/api/v1", "response_time": 1.5, "http_user_agent": "Mozilla/5.0"}',
        '{"@timestamp": "2023-10-02T12:00:00Z", "url": "/api/v2", "response_time": 1.0, "http_user_agent": "Chrome/1.0"}'
    ]
    file = tmp_path / "logs.json"
    file.write_text("\n".join(data) + "\n")
    return str(file)


@pytest.fixture
def invalid_json_file(tmp_path):
    data = [
        '{"@timestamp": "2023-10-01T12:00:00Z", "url": "/api/v1", "response_time": 0.5}',
        'Invalid JSON line'
    ]
    file = tmp_path / "invalid.json"
    file.write_text("\n".join(data) + "\n")
    return str(file)


@pytest.fixture
def missing_timestamp_file(tmp_path):
    data = [
        '{"url": "/api/v1", "response_time": 0.5}'
    ]
    file = tmp_path / "missing_ts.json"
    file.write_text("\n".join(data) + "\n")
    return str(file)


@pytest.fixture
def invalid_timestamp_file(tmp_path):
    data = [
        '{"@timestamp": "invalid-date", "url": "/api/v1", "response_time": 0.5}'
    ]
    file = tmp_path / "invalid_ts.json"
    file.write_text("\n".join(data) + "\n")
    return str(file)

@pytest.fixture
def mock_reports():
    return {
        "mock_report": lambda logs: ([["data1", "data2"], ["data3", "data4"]], ["Header1", "Header2"])
    }


@pytest.fixture
def logs():
    return {"log_key": "log_value"}


def test_load_logs_valid(sample_log_file, capsys):
    logs = list(loader.load_logs([sample_log_file]))
    assert len(logs) == 3
    captured = capsys.readouterr()
    assert captured.out == ""


def test_load_logs_invalid_json(invalid_json_file, capsys):

    with pytest.raises(exceptionts.JSONDecodeError, match="Invalid JSON in file"):
        list(loader.load_logs([invalid_json_file]))


def test_load_logs_missing_timestamp(missing_timestamp_file, capsys):
    date_filter = datetime(2023, 10, 1).date()

    with pytest.raises(exceptionts.MissingKeyError, match="Missing '@timestamp' key in log"):
        list(loader.load_logs([missing_timestamp_file], date_filter))



def test_load_logs_invalid_timestamp(invalid_timestamp_file, capsys):
    date_filter = datetime(2023, 10, 1).date()

    with pytest.raises(exceptionts.InvalidKeyError, match="Invalid timestamp format"):
        list(loader.load_logs([invalid_timestamp_file], date_filter))


def test_load_logs_date_filter(sample_log_file):
    date_filter = datetime(2023, 10, 1).date()
    logs = list(loader.load_logs([sample_log_file], date_filter))
    assert len(logs) == 2


def test_generate_average_report(capsys):
    logs = [
        {"url": "/api/v1", "response_time": 0.5},
        {"url": "/api/v1", "response_time": 1.5},
        {"url": "/api/v2", "response_time": 1.0}
    ]
    table_data, headers = report_generators.generate_average_report(logs)
    assert headers == ['Endpoint', 'Count', 'Average']
    assert table_data == [
        ["/api/v1", 2, 1.0],
        ["/api/v2", 1, 1.0]
    ]
    captured = capsys.readouterr()
    assert captured.out == ""


def test_generate_average_report_missing_url(capsys):
    logs = [{"response_time": 0.5}]

    with pytest.raises(exceptionts.MissingKeyError,
                       match=" Missing url key in a log entry"):
        report_generators.generate_average_report(logs)



def test_generate_average_report_invalid_response_time(capsys):
    logs = [{"url": "/api", "response_time": "not a number"}]

    with pytest.raises(exceptionts.InvalidKeyError,
                       match="response_time must be a number"):
        report_generators.generate_average_report(logs)


def test_generate_user_agent_report(capsys):
    logs = [
        {"http_user_agent": "Mozilla/5.0"},
        {"http_user_agent": "Mozilla/5.0"},
        {"http_user_agent": "Chrome/1.0"}
    ]
    table_data, headers = report_generators.generate_user_agent_report(logs)
    assert headers == ['User-Agents', 'Count']
    assert table_data == [
        ["Mozilla/5.0", 2],
        ["Chrome/1.0", 1]
    ]
    captured = capsys.readouterr()
    assert captured.out == ""


def test_generate_user_agent_report_empty():
    logs = []
    table_data, _ = report_generators.generate_user_agent_report(logs)
    assert len(table_data) == 0


def test_user_agent_report_with_empty_file_flag(capsys, caplog):
    test_args = ["main.py", "--file", "--report", "User-Agents"]

    with patch.object(sys, 'argv', test_args):
        main()

    # Проверка предупреждения в логах
    assert "Incorrect flag" in caplog.text

    # Проверка, что в стандартном выводе нет сообщения об ошибке
    captured = capsys.readouterr()
    assert "Error: Invalid command-line" not in captured.out


def test_average_report_with_empty_file_flag(capsys, caplog):
    test_args = ["main.py", "--file", "--report", "average"]

    with patch.object(sys, 'argv', test_args):
        main()

    # Проверка предупреждения в логах
    assert "Incorrect flag" in caplog.text

    # Проверка, что в стандартном выводе нет сообщения об ошибке
    captured = capsys.readouterr()
    assert "Error: Invalid command-line" not in captured.out



def test_report_table_file_not_found(mock_reports, logs):
    args = Mock()
    args.report = "non_existent_report"

    with pytest.raises(KeyError):
        report_table(args, mock_reports, logs)


def test_report_table_missing_key_error(mock_reports, logs):
    reports_with_error = {
        "mock_report": lambda logs: (_ for _ in ()).throw(exceptionts.MissingKeyError("Missing key"))
    }

    args = Mock()
    args.report = "mock_report"

    with pytest.raises(exceptionts.MissingKeyError):
        report_table(args, reports_with_error, logs)


def test_report_table_invalid_key_error(mock_reports, logs):
    reports_with_error = {
        "mock_report": lambda logs: (_ for _ in ()).throw(exceptionts.InvalidKeyError("Invalid key"))
    }

    args = Mock()
    args.report = "mock_report"

    with pytest.raises(exceptionts.InvalidKeyError):
        report_table(args, reports_with_error, logs)

