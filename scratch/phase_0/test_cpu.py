import psutil, datetime as dt

current_time = dt.datetime.now()

cpu_usage = psutil.cpu_percent(interval=1)
ram_usage = psutil.virtual_memory().percent
print(f"\n[timestamp: {current_time}] CPU & RAM usage of this system: {cpu_usage}%, {ram_usage}%\n")