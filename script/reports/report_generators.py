from collections import defaultdict
from typing import Dict, List, Tuple, Union
from exceptionts import MissingKeyError, InvalidKeyError

TIMESTAMP = "@timestamp"
STATUS = "status"
URL = "url"
REQUEST_METHOD = "request_method"
RESPONSE_TIME = "response_time"
USER_AGENT = "http_user_agent"

COUNT = 'count'
TOTAL_TIME = "total_time"


LogEntry = Dict[str, Union[str, int, float]]

def generate_average_report(
        logs: List[LogEntry]
) -> Tuple[List[List[Union[str, int, float]]], List[str]]:

    endpoint_data = defaultdict(
        lambda: {
            COUNT: 0,
            TOTAL_TIME: 0.0
        }
    )
    for log in logs:
        try:
            url = log[URL]
        except KeyError:
            raise MissingKeyError("Error: Missing %s key in a log entry" % URL)

        try:
            response_time = log.get(RESPONSE_TIME , 0.0)
        except KeyError:
            raise MissingKeyError("Error: Missing %s key in a log entry" % RESPONSE_TIME)

        if not isinstance(response_time, (int, float)):
            raise InvalidKeyError(message="%s must be a number" % RESPONSE_TIME)

        endpoint_data[url][COUNT] += 1
        endpoint_data[url][TOTAL_TIME] += response_time


    table_data = []
    for url, data in endpoint_data.items():
        avg_time = data[TOTAL_TIME] / data[COUNT] \
            if data[COUNT] > 0 \
            else 0.0
        table_data.append([url, data[COUNT], round(avg_time, 3)])

    table_data.sort(key=lambda x: (-x[2], -x[1]))

    return table_data, ['Endpoint', 'Count', 'Average']


def generate_user_agent_report(
        logs: List[LogEntry]
) -> Tuple[List[List[Union[str, int]]], List[str]]:
    user_agent_data = defaultdict(int)

    for log in logs:
        user_agent = log.get(USER_AGENT , '')
        user_agent_data[user_agent] += 1
    table_data = [
        [agent, count] for agent, count in sorted(
            user_agent_data.items(),
            key=lambda x: x[1], reverse=True
        )
    ]

    return table_data, ['User-Agent', 'Count']
