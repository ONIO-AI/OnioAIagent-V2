# task_base.py
class Task:
    def __init__(self, name):
        self.name = name

    def run(self):
        raise NotImplementedError("Subclasses must implement the 'run' method.")
