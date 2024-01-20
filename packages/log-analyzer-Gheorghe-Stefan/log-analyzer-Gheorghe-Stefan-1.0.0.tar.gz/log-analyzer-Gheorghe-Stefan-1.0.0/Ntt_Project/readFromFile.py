import re
def readFile(path):
    # './output.txt'
    with open(path, 'r') as file:
        lines = file.readlines()
    return lines

def extractData(log_lines):

    compiled_logs = []

    ERROR_log_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - (\w+) has (.+?) after (\d+)ms.?.*')
    DEBUG_log_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - (\w+) is still running, please wait...*')
    INFO1_log_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - (\w+) has started running...*')
    INFO2_log_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}) - \[([A-Z]+)\] - (\w+) has (.+?) in (\d+)ms.?.*')

    for log_line in log_lines:
        ERROR_match = ERROR_log_pattern.match(log_line)
        DEBUG_match = DEBUG_log_pattern.match(log_line)
        INFO1_match = INFO1_log_pattern.match(log_line)
        INFO2_match = INFO2_log_pattern.match(log_line)
        if ERROR_match:
            timestamp, log_type, app, status, run_time = ERROR_match.groups()
            compiled_logs.append({"timestamp": timestamp, "log_type": log_type, "app": app, "status": -1, "run_time": run_time})
        elif DEBUG_match:
            timestamp, log_type, app = DEBUG_match.groups()
            compiled_logs.append({"timestamp": timestamp, "log_type": log_type, "status": 0, "app": app})
        elif INFO1_match:
            timestamp, log_type, app = INFO1_match.groups()
            compiled_logs.append({"timestamp": timestamp, "log_type": log_type, "status": 0, "app": app})
        elif INFO2_match:
            timestamp, log_type, app, status, run_time = INFO2_match.groups()
            compiled_logs.append({"timestamp": timestamp, "log_type": log_type, "app": app, "status": 1, "run_time": run_time})

    return compiled_logs


