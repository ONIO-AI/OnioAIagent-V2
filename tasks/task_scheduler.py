# task_scheduler.py
import time
from threading import Thread

class TaskScheduler:
    def __init__(self):
        self.scheduled_tasks = []

    def schedule_task(self, task, interval):
        def run_task():
            while True:
                task.run()
                time.sleep(interval)
        thread = Thread(target=run_task)
        thread.start()
