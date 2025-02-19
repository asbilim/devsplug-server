import multiprocessing

bind = "0.0.0.0:10000"  # Render expects port 10000
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 120
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
capture_output = True
enable_stdio_inheritance = True 