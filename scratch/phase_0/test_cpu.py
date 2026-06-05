import psutil

cpu_usage = psutil.cpu_percent(interval=1)
print(f"El uso actual de la CPU de mi PC es del: {cpu_usage}%")