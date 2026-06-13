import psutil, datetime as dt
import csv


def main(): 
    stats()
    with open("hardware_log.csv", "a") as f:
        writer = csv.DictWriter(f)
        writer.writerow(stats())

def stats(): 
    current_time = dt.datetime.now()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    log = {
        "timestamp": current_time, 
        "CPU_usage": cpu_usage,
        "RAM_usage": ram_usage,
    }
    return log

main()