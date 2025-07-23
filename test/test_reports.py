import pytest
from datetime import datetime

from script import loader
from script import report_generators


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


def test_load_logs_valid(sample_log_file, capsys):
    logs = list(loader.load_logs([sample_log_file]))
    assert len(logs) == 3
    captured = capsys.readouterr()
    assert captured.out == ""


def test_load_logs_invalid_json(invalid_json_file, capsys):
    logs = list(loader.load_logs([invalid_json_file]))
    assert len(logs) == 1
    captured = capsys.readouterr()
    assert "Error: Invalid JSON" in captured.out


def test_load_logs_missing_timestamp(missing_timestamp_file, capsys):
    date_filter = datetime(2023, 10, 1).date()
    logs = list(loader.load_logs([missing_timestamp_file], date_filter))
    assert len(logs) == 0
    captured = capsys.readouterr()
    assert "Error: Missing '@timestamp' key" in captured.out


def test_load_logs_invalid_timestamp(invalid_timestamp_file, capsys):
    date_filter = datetime(2023, 10, 1).date()
    logs = list(loader.load_logs([invalid_timestamp_file], date_filter))
    assert len(logs) == 0
    captured = capsys.readouterr()
    assert "Error: Invalid timestamp format" in captured.out


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
    table_data, _ = report_generators.generate_average_report(logs)
    assert len(table_data) == 0
    captured = capsys.readouterr()
    assert "Error: Missing 'url' key" in captured.out


def test_generate_average_report_invalid_response_time(capsys):
    logs = [{"url": "/api", "response_time": "not a number"}]
    table_data, _ = report_generators.generate_average_report(logs)
    assert len(table_data) == 0
    captured = capsys.readouterr()
    assert "Error in log processing: response_time must be a number" in captured.out


def test_generate_user_agent_report(capsys):
    logs = [
        {"http_user_agent": "Mozilla/5.0"},
        {"http_user_agent": "Mozilla/5.0"},
        {"http_user_agent": "Chrome/1.0"}
    ]
    table_data, headers = report_generators.generate_user_agent_report(logs)
    assert headers == ['User-Agent', 'Count']
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
