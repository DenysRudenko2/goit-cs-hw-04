import multiprocessing
import logging
# import queue
# from collections import defaultdict
from pathlib import Path
import timeit
import os

def search_in_file(file_path, keywords, results_queue):
  try:
    with open(file_path, 'r') as file:
      content = file.read()
      for keyword in keywords:
        if keyword in content:
          results_queue.put((keyword, file_path))
  except IOError as e:
    logging.error(f"Error {file_path}: {e}")

def process_task(files, keywords, results_queue):
  for file in files:
    search_in_file(file, keywords, results_queue)

def main_multiprocessing(file_paths, keywords): 
  start_time = timeit.default_timer()
  num_processes = os.cpu_count()
  results_queue = multiprocessing.Queue()

  files_per_process = len(file_paths) // num_processes
  processes = []

  for i in range(num_processes):
    start = i * files_per_process
    end = None if i == num_processes - 1 else start + files_per_process
    files_for_process = file_paths[start:end]

    process = multiprocessing.Process(target=process_task, args= (files_for_process, keywords, results_queue))
    processes.append(process)
    process.start()

  for process in processes:
    process.join()

  results = {}
  while not results_queue.empty():
    keyword, file_path, = results_queue.get()
    if keyword in results:
      results[keyword].append(file_path)
    else:
      results[keyword] = [file_path]

  print(f"Time in multiprocessing - {timeit.default_timer() - start_time}s")

  return results

if __name__ == '__main__':
  file_paths = list(Path("input").glob("*.txt"))
  print(f"File paths: {file_paths}\n")
  keywords = ['lorem', 'doloremque', 'ipsa']
  results = main_multiprocessing(file_paths, keywords)
  print(results)