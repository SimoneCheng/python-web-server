# 嘗試用 multithreading 寫費氏數列的 function，想法：
# 一個 thread 搜集所有 input
# 另外一個 thread 做費氏數列的運算
# 用 global variable 做 cache，因為兩個 thread 在同一個 process 裡面

import threading
from queue import Queue

def fibonacci(value):
  if (value == 0):
    return 0
  elif (value == 1):
    return 1
  else:
    return fibonacci(value - 1) + fibonacci(value - 2)

fibonacci_cache = {}
all_input_queue = Queue()
queue_condition = threading.Condition()
input_example = [1, 2, 3, 4, 5, 5, 7, 8, 9, 10]

def fibonacci_task(condition):
  with condition:
    while all_input_queue.empty():
      print("Waiting for elements in queue...")
      condition.wait()
    else:
      value = all_input_queue.get()
      if value in fibonacci_cache:
        print("value in cache", fibonacci_cache[value])
      else:
        result = fibonacci(value)
        fibonacci_cache.update({ value: result })
        print("value not in cache", result)
    all_input_queue.task_done()

def input_task(condition):
  with condition:
    for item in input_example:
      all_input_queue.put(item)
    print(all_input_queue.qsize())
    print("Notifying fibonacci task thread that the queue is ready to consume...")
    condition.notify_all()

input_threads = threading.Thread(target=input_task, args=(queue_condition,))
input_threads.start()

threads = []
for _ in range(10):
  thread = threading.Thread(target=fibonacci_task, args=(queue_condition,))
  threads.append(thread)

[thread.start() for thread in threads]
[thread.join() for thread in threads]
