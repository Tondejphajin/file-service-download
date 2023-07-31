import multiprocessing
import subprocess

# get number of available CPUs
num_cpus = multiprocessing.cpu_count()
print(num_cpus)

# start celery worker with concurrency equals to number of CPUs
command = f"celery -A worker worker --concurrency={num_cpus}"

# Using subprocess to run the command
process = subprocess.run(command, shell=True, check=True)
print(command)
