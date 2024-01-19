import time
import configparser
import platform
import socket
import json
import psutil
import logging
import os
from datetime import datetime

def getSystemInfo():
    try:
        info={}
        info['sys_platform']=platform.system()
        info['sys_platform_release']=platform.release()
        info['sys_platform_version']=platform.version()
        info['sys_architecture']=platform.machine()
        info['sys_hostname']=socket.gethostname()
        info['sys_processor']=platform.processor()
        info['sys_ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['sys_ncpu']=psutil.cpu_count(logical=False)
        info['sys_cpu_max_freq'] = psutil.cpu_freq().max
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def benchmark(func):
    def decorated_func():
        exec_time = datetime.now()
        timefmt = "%Y-%m-%d_%H-%M-%S"
        exec_time = exec_time.strftime(timefmt)

        system_info = json.loads(getSystemInfo())
        benchmark_test = {
            "time": exec_time,
        }

        print(
            f"Starting Benchmark("
            f"time={datetime.strptime(benchmark_test['time'], timefmt)}, "
            ")"
        )

        # Execute benchmark
        cpu_time_start = time.process_time()
        wall_time_start = time.time()

        func()

        cpu_time_stop = time.process_time()
        wall_time_stop = time.time()

        # record result of Benchmark
        cpu_time = cpu_time_stop - cpu_time_start
        wall_time = wall_time_stop - wall_time_start

        result = {
            "walltime_s": wall_time,
            "cputime_s": cpu_time,
        }

        # Update Benchmarking results table
        benchmark_test.update(result)
        benchmark_test.update(system_info)

        print(
            f"Finished Benchmark("
            f"runtime={result['walltime_s']}s, "
            f"cputime={result['cputime_s']}s, "
            f"ncores={benchmark_test['sys_ncpu']}"
        )
        return benchmark_test
    
    return decorated_func
