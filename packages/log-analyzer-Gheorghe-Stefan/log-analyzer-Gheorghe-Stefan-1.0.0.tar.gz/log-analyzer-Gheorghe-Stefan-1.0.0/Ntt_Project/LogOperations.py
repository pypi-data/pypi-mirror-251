import operator
from .readFromFile import readFile, extractData


class LogOperations:
    def ex1(self, path):
        logs = extractData(readFile(path))

        info_logs = [0, 0, 0, 0]
        debug_logs = [0, 0, 0, 0]
        error_logs = [0, 0, 0, 0]

        for log in logs:
            if log["log_type"] == "INFO":
                if log["app"] == "API":
                    info_logs[0] += 0.5
                elif log["app"] == "FrontendApp":
                    info_logs[1] += 0.5
                elif log["app"] == "BackendApp":
                    info_logs[2] += 0.5
                elif log["app"] == "SYSTEM":
                    info_logs[3] += 0.5

            elif log["log_type"] == "DEBUG":
                if log["app"] == "API":
                    debug_logs[0] += 1
                elif log["app"] == "FrontendApp":
                    debug_logs[1] += 1
                elif log["app"] == "BackendApp":
                    debug_logs[2] += 1
                elif log["app"] == "SYSTEM":
                    debug_logs[3] += 1

            elif log["log_type"] == "ERROR":
                if log["app"] == "API":
                    error_logs[0] += 1
                elif log["app"] == "FrontendApp":
                    error_logs[1] += 1
                elif log["app"] == "BackendApp":
                    error_logs[2] += 1
                elif log["app"] == "SYSTEM":
                    error_logs[3] += 1

        dict1 = {"API": int(info_logs[0]),
                 "Frontend": int(info_logs[1]),
                 "Backend": int(info_logs[2]),
                 "System": int(info_logs[3])}
        dict2 = {"API": int(debug_logs[0]),
                 "Frontend": int(debug_logs[1]),
                 "Backend": int(debug_logs[2]),
                 "System": int(debug_logs[3])}
        dict3 = {"API": int(error_logs[0]),
                 "Frontend": int(error_logs[1]),
                 "Backend": int(error_logs[2]),
                 "System": int(error_logs[3])}

        dict = {"INFO": dict1,
                "DEBUG": dict2,
                "ERROR": dict3}

        # print(dict)

        return dict

    def ex2(self, path):
        logs = extractData(readFile(path))

        front = 0
        frontTime = 0
        end = 0
        endTime = 0
        api = 0
        apiTime = 0

        for log in logs:
            if "run_time" in log:
                if "status" in log and log["status"] == 1:
                    if "FrontendApp" == log['app']:
                        front += 1
                        frontTime += int(log['run_time'])
                    elif "BackendApp" == log['app']:
                        end += 1
                        endTime += int(log['run_time'])
                    elif "API" == log['app']:
                        api += 1
                        apiTime += int(log['run_time'])

        # print("Front: " + str(front) + " - " + str(frontTime/front))
        # print("End: " + str(end) + " - " + str(endTime/end))
        # print("API: " + str(api) + " - " + str(apiTime/api))

        return front, frontTime / front, end, endTime / end, api, apiTime / api

    def ex3(self, path):
        logs = extractData(readFile(path))

        failed_front_number = 0
        failed_end_number = 0
        failed_api_number = 0
        failed_system_number = 0

        for log in logs:
            if "status" in log and log["status"] == -1:
                if "FrontendApp" == log['app']:
                    failed_front_number += 1
                elif "BackendApp" == log['app']:
                    failed_end_number += 1
                elif "API" == log['app']:
                    failed_api_number += 1
                elif "SYSTEM" == log['app']:
                    failed_system_number += 1

        # print("Failed front: " + str(failed_front_number))
        # print("Failed end: " + str(failed_end_number))
        # print("Failed API: " + str(failed_api_number))
        # print("Failed system: " + str(failed_system_number))

        return failed_front_number, failed_end_number, failed_api_number, failed_system_number

    def ex4(self, path):
        logs = extractData(readFile(path))

        api_fails_number = 0
        backend_fails_number = 0
        frontend_fails_number = 0
        sys_fails_number = 0

        for log in logs:
            if "status" in log and log["status"] == -1:
                if "FrontendApp" == log['app']:
                    frontend_fails_number += 1
                elif "BackendApp" == log['app']:
                    backend_fails_number += 1
                elif "API" == log['app']:
                    api_fails_number += 1
                elif "SYSTEM" == log['app']:
                    sys_fails_number += 1

        my_dict = {"API": api_fails_number,
                   "Frontend": frontend_fails_number,
                   "System": sys_fails_number,
                   "BackendApp": backend_fails_number}

        sorted_dict = dict(sorted(my_dict.items(), key=operator.itemgetter(1), reverse=True))
        # print(next(iter(sorted_dict)), sorted_dict.get(next(iter(sorted_dict))))

        return next(iter(sorted_dict)), sorted_dict.get(next(iter(sorted_dict)))

    def ex5(self, path):
        logs = extractData(readFile(path))

        api_suc_number = 0
        backend_suc_number = 0
        frontend_suc_number = 0
        sys_suc_number = 0

        for log in logs:
            if "status" in log and log["status"] == 1:
                if "FrontendApp" == log['app']:
                    frontend_suc_number += 1
                elif "BackendApp" == log['app']:
                    backend_suc_number += 1
                elif "API" == log['app']:
                    api_suc_number += 1
                elif "SYSTEM" == log['app']:
                    sys_suc_number += 1

        my_dict = {"API": api_suc_number,
                   "Frontend": frontend_suc_number,
                   "System": sys_suc_number,
                   "BackendApp": backend_suc_number}

        sorted_dict = dict(sorted(my_dict.items(), key=operator.itemgetter(1), reverse=True))
        # print(next(iter(sorted_dict)), sorted_dict.get(next(iter(sorted_dict))))

        return next(iter(sorted_dict)), sorted_dict.get(next(iter(sorted_dict)))

    def ex6(self, path):
        logs = extractData(readFile(path))

        fails = [0, 0, 0]

        for log in logs:
            if "status" in log and log["status"] == -1:
                if log["timestamp"] < "08:00:00":
                    fails[0] += 1
                elif log["timestamp"] < "16:00:00":
                    fails[1] += 1
                else:
                    fails[2] += 1

        if max(fails) == fails[0]:
            print("Most fails in: 00:00:00 - 07:59:59 in total: " + str(fails[0]))
            return fails[0]
        elif max(fails) == fails[1]:
            print("Most fails in: 08:00:00 - 15:59:59 in total: " + str(fails[1]))
            return fails[1]
        elif max(fails) == fails[2]:
            print("Most fails in: 16:00:00 - 23:59:59 in total: " + str(fails[2]))
            return fails[2]

    def ex7(self, path):
        logs = extractData(readFile(path))

        shortest_runtime_api = []
        shortest_runtime_backend = []
        shortest_runtime_frontend = []
        longest_runtime_api = []
        longest_runtime_backend = []
        longest_runtime_frontend = []

        min_api = -1
        min_backend = -1
        min_frontend = -1

        max_api = -1
        max_backend = -1
        max_frontend = -1

        sorted_log_entries = sorted(logs, key=lambda x: int(x.get('run_time', 0)))

        for log in sorted_log_entries:
            if "status" in log and log["status"] == 1:
                if log["app"] == "API":
                    if min_api == -1:
                        min_api = int(log['run_time'])
                        shortest_runtime_api.append(log)
                    elif min_api == int(log['run_time']):
                        shortest_runtime_api.append(log)
                    elif min_api > int(log['run_time']):
                        min_api = int(log['run_time'])
                        shortest_runtime_api.clear()
                        shortest_runtime_api.append(log)
                    if max_api < int(log['run_time']):
                        max_api = int(log['run_time'])
                        longest_runtime_api.clear()
                        longest_runtime_api.append(log)
                    elif max_api == int(log['run_time']):
                        longest_runtime_api.append(log)
                elif log["app"] == "FrontendApp":
                    if min_frontend == -1:
                        min_frontend = int(log['run_time'])
                        shortest_runtime_frontend.append(log)
                    elif min_frontend == int(log['run_time']):
                        shortest_runtime_frontend.append(log)
                    elif min_frontend > int(log['run_time']):
                        min_frontend = int(log['run_time'])
                        shortest_runtime_frontend.clear()
                        shortest_runtime_frontend.append(log)
                    if max_frontend < int(log['run_time']):
                        max_frontend = int(log['run_time'])
                        longest_runtime_frontend.clear()
                        longest_runtime_frontend.append(log)
                    elif max_frontend == int(log['run_time']):
                        longest_runtime_frontend.append(log)
                elif log["app"] == "BackendApp":
                    if min_backend == -1:
                        min_backend = int(log['run_time'])
                        shortest_runtime_backend.append(log)
                    elif min_backend == int(log['run_time']):
                        shortest_runtime_backend.append(log)
                    elif min_backend > int(log['run_time']):
                        min_backend = int(log['run_time'])
                        shortest_runtime_backend.clear()
                        shortest_runtime_backend.append(log)
                    if max_backend < int(log['run_time']):
                        max_backend = int(log['run_time'])
                        longest_runtime_backend.clear()
                        longest_runtime_backend.append(log)
                    elif max_backend == int(log['run_time']):
                        longest_runtime_backend.append(log)

        # for log in shortest_runtime_api:
        #     print("API shortest runtime: " + log["timestamp"] + " - " + log["run_time"])
        # for log in shortest_runtime_frontend:
        #     print("Frontend shortest runtime: " + log["timestamp"] + " - " + log["run_time"])
        # for log in shortest_runtime_backend:
        #     print("Backend shortest runtime: " + log["timestamp"] + " - " + log["run_time"])
        #
        # for log in longest_runtime_api:
        #     print("API longest runtime: " + log["timestamp"] + " - " + log["run_time"])
        # for log in longest_runtime_frontend:
        #     print("Frontend longest runtime: " + log["timestamp"] + " - " + log["run_time"])
        # for log in longest_runtime_backend:
        #     print("Backend longest runtime: " + log["timestamp"] + " - " + log["run_time"])

        return shortest_runtime_api, shortest_runtime_backend, shortest_runtime_frontend, longest_runtime_api, longest_runtime_backend, longest_runtime_frontend

    def ex8(self, path):
        logs = extractData(readFile(path))

        sorted_log_entries = sorted(logs, key=lambda x: x.get('timestamp'))
        dict = {}

        max_api = 0
        max_frontend = 0
        max_backend = 0

        max_api_time = "00"
        max_frontend_time = "00"
        max_backend_time = "00"

        api = 0
        frontend = 0
        backend = 0

        current_time = "00"

        for log in sorted_log_entries:
            if current_time != log["timestamp"][:2]:
                current_time = log["timestamp"][:2]
                if api >= frontend and api >= backend:
                    dict[current_time] = "API"
                    if api > max_api:
                        max_api = api
                        max_api_time = current_time

                elif frontend >= api and frontend >= backend:
                    dict[current_time] = "Frontend"
                    if frontend > max_frontend:
                        max_frontend = frontend
                        max_frontend_time = current_time

                elif backend >= api and backend >= frontend:
                    dict[current_time] = "Backend"
                    if backend > max_backend:
                        max_backend = backend
                        max_backend_time = current_time

                api = 0
                frontend = 0
                backend = 0

            if log["log_type"] == "INFO" and log["app"] == "API":
                api += 0.5
            else:
                api += 1
            if log["log_type"] == "INFO" and log["app"] == "FrontendApp":
                frontend += 0.5
            else:
                frontend += 1
            if log["log_type"] == "INFO" and log["app"] == "BackendApp":
                backend += 0.5
            else:
                backend += 1

        # print(dict)
        max_activity_timestamps = {"API": max_api_time, "Frontend": max_frontend_time, "Backend": max_backend_time}
        return max_activity_timestamps

    def ex9(self, path):
        dict = LogOperations.ex1(self, path)
        total_logs_front = dict["INFO"]["Frontend"] + dict["DEBUG"]["Frontend"] + dict["ERROR"]["Frontend"]
        total_logs_end = dict["INFO"]["Backend"] + dict["DEBUG"]["Backend"] + dict["ERROR"]["Backend"]
        total_logs_api = dict["INFO"]["API"] + dict["DEBUG"]["API"] + dict["ERROR"]["API"]
        total_logs_system = dict["INFO"]["System"] + dict["DEBUG"]["System"] + dict["ERROR"]["System"]

        # print("Frontend failure rate: " + str(dict["ERROR"]["Frontend"] / total_logs_front * 100) + "%")
        # print("Backend failure rate: " + str(dict["ERROR"]["Backend"] / total_logs_end * 100) + "%")
        # print("API failure rate: " + str(dict["ERROR"]["API"] / total_logs_api * 100) + "%")
        # print("System failure rate: " + str(dict["ERROR"]["System"] / total_logs_system * 100) + "%")

        percentage = {"Frontend": dict["ERROR"]["Frontend"] / total_logs_front * 100,
                      "Backend": dict["ERROR"]["Backend"] / total_logs_end * 100,
                      "API": dict["ERROR"]["API"] / total_logs_api * 100,
                      "System": dict["ERROR"]["System"] / total_logs_system * 100}

        return percentage


logOperations = LogOperations()
