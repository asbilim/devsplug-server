import multiprocessing

# Calculate workers based on CPU cores, but with a reasonable maximum
def get_workers():
    cores = multiprocessing.cpu_count()
    # Use 2-4 workers per core, but cap at 8 total
    return min(cores * 2, 8)

bind = "0.0.0.0:10000"  # Render expects port 10000
workers = get_workers()
worker_class = "gthread"  # Using threads for better performance
threads = 4
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
loglevel = "debug"
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
capture_output = True
enable_stdio_inheritance = True 