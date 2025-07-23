from collections import defaultdict


def generate_average_report(logs):
    endpoint_data = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    for log in logs:
        try:
            url = log['url']
            response_time = log.get('response_time', 0.0)
            if not isinstance(response_time, (int, float)):
                raise ValueError("response_time must be a number")
            endpoint_data[url]['count'] += 1
            endpoint_data[url]['total_time'] += response_time
        except KeyError:
            print("Error: Missing 'url' key in a log entry")
        except ValueError as e:
            print("Error in log processing: %s" % e)

    table_data = []
    for url, data in sorted(endpoint_data.items()):
        avg_time = data['total_time'] / data['count'] \
            if data['count'] > 0 \
            else 0.0
        table_data.append([url, data['count'], round(avg_time, 3)])

    return table_data, ['Endpoint', 'Count', 'Average']


def generate_user_agent_report(logs):
    user_agent_data = defaultdict(int)

    for log in logs:
        user_agent = log.get('http_user_agent', '')
        user_agent_data[user_agent] += 1
    table_data = [
        [agent, count] for agent, count in sorted(
            user_agent_data.items(),
            key=lambda x: x[1], reverse=True
        )
    ]

    return table_data, ['User-Agent', 'Count']
