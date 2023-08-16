#!/usr/bin/env python3

__author__ = "Rodrigo H Padilla"
__email__ = "rod.hpadilla@gmail.com"


import time
from subprocess import Popen, DEVNULL
from threading import Thread
from rich.console import Console
from rich.table import Table
import itertools


DEVICE_FILE = "devices.txt"
TIME = time.asctime(time.localtime(time.time()))
SUCCESS_LIST = []
FAIL_LIST = []
with open(DEVICE_FILE) as f:
    DEVICE_LIST = f.read().splitlines()


def runner(device) -> None:
    try:
        ping_result = Popen(["ping", "-c", "3", "-i", "0.2", device], stdout=DEVNULL)
        time.sleep(2)
        ping_result.poll()
        if ping_result.returncode == 0:
            SUCCESS_LIST.append(device)
        elif ping_result.returncode == 1:
            FAIL_LIST.append(device)
        else:
            FAIL_LIST.append(device)
    except Exception:
        FAIL_LIST.append(device)


def report() -> None:
    try:
        table = Table(title="CONNECTIVITY REPORT \n" + TIME)
        table.add_column("SUCCESS DEVICES", justify="center", style="green")
        table.add_column("FAILED DEVICES", justify="center",style="red")
        for (a,i) in itertools.zip_longest(SUCCESS_LIST,FAIL_LIST):
            table.add_row(a,i)
        console = Console()
        console.print(table)
    except Exception:
        return False


if __name__ == "__main__":

    threads = []
    if len(DEVICE_LIST) > 0:
        for device_item in DEVICE_LIST:
            t = Thread(target=runner, args=(device_item,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
    
    if len(SUCCESS_LIST) > 0 or len(FAIL_LIST) > 0:
        report()
    else:
        print("nothing to run")

