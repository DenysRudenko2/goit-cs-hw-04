import threading
import logging
from collections import defaultdict
from pathlib import Path
import time

def search_in_file(file_path, keywords, results_queue):
  try:
    with open(file_path, 'r') as file:
      content = file.read()
    for keyword in keywords:
      if keyword in content:
        results_queue[keyword].append(file_path)
  except IOError as e:
    logging.error(f"Error {file_path}: {e}")

def thread_task(files, keywords, results_queue):
  for file in files:
    search_in_file(file, keywords, results_queue)

def main_threading(file_paths, keywords):
  start_time = time.time()
  num_threads = 4
  threads = []
  results = defaultdict(list)
  files_per_thread = len(file_paths) // num_threads

  for i in range(num_threads):
    start = i * files_per_thread
    end = None if i == num_threads - 1 else start + files_per_thread
    files_for_thread = file_paths[start:end]

    thread = threading.Thread(target = thread_task, args=(files_for_thread, keywords, results))

    threads.append(thread)
    thread.start()

  for thread in threads:
    thread.join()

  print(f"Time in threading - {time.time() - start_time}s")

  return results

if __name__ == '__main__':
  file_paths = list(Path("input").glob("*.txt"))
  print(f"File paths: {file_paths}\n")
  keywords = ['lorem', 'doloremque', 'ipsa']
  results = main_threading(file_paths, keywords)
  print(results)